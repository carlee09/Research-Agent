"""X (Twitter) data collector using Sela Network API."""

import time
from typing import List, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .base import BaseCollector
from src.config import Config


class XCollector(BaseCollector):
    """Collector for X (Twitter) data via Sela Network API."""

    def __init__(self):
        """Initialize X collector with Sela Network API credentials."""
        super().__init__(
            api_key=Config.SELA_API_KEY,
            api_url=Config.SELA_API_ENDPOINT
        )
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """
        Create requests session with retry logic.

        Returns:
            Configured requests session
        """
        session = requests.Session()
        retry = Retry(
            total=Config.MAX_RETRIES,
            backoff_factor=Config.RETRY_DELAY,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def collect(self, topic: str, max_items: int = 20) -> List[Dict[str, Any]]:
        """
        Collect X (Twitter) posts for the given topic.

        Args:
            topic: Research topic
            max_items: Maximum number of posts to collect

        Returns:
            List of collected posts with metadata
        """
        self.logger.info(f"🔍 Collecting X data for topic: '{topic}'")

        try:
            # For topic research, scrape relevant Twitter profiles
            # Map common topics to relevant Twitter accounts
            topic_accounts = {
                "uniswap": "Uniswap",
                "ethereum": "ethereum",
                "bitcoin": "Bitcoin",
                "crypto": "CoinDesk",
            }

            # Try to find a relevant account, otherwise use a default
            topic_lower = topic.lower()
            account = None
            for key, username in topic_accounts.items():
                if key in topic_lower:
                    account = username
                    break

            # If no specific account found, use the topic as account name
            if not account:
                # Clean topic for use as account name (remove spaces, special chars)
                account = topic.replace(" ", "").replace("#", "").replace("@", "")

            profile_url = f"https://twitter.com/{account}"

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "url": profile_url,
                "scrapeType": "TWITTER_PROFILE",
                "timeoutMs": 60000,  # 1 minute
                "postCount": max_items,
                "scrollPauseTime": 2000
            }

            self.logger.debug(f"Request payload: {payload}")

            response = self.session.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=120  # 2 minutes timeout (longer than timeoutMs)
            )

            self.logger.info(f"Response status: {response.status_code}")
            if response.status_code != 200:
                self.logger.error(f"Error response: {response.text}")

            response.raise_for_status()

            data = response.json()

            if not data.get("success"):
                self.logger.error(f"❌ API returned success=false: {data.get('message')}")
                return []

            results = self._parse_x_response(data, max_items)

            self.logger.info(f"✅ Collected {len(results)} X posts")
            return results

        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Error collecting X data: {e}")
            return []

    def _parse_x_response(self, data: Dict[str, Any], max_items: int) -> List[Dict[str, Any]]:
        """
        Parse Sela Network X API response.

        Args:
            data: Raw API response
            max_items: Maximum items to return

        Returns:
            List of formatted posts
        """
        results = []

        try:
            result_data = data.get("data", {}).get("result", {})

            # Handle different possible response structures
            posts = []
            if isinstance(result_data, dict):
                # Check for common keys that might contain tweet data
                posts = (result_data.get("tweets") or
                        result_data.get("posts") or
                        result_data.get("results") or
                        result_data.get("items") or [])

                # If result is a single tweet/post
                if "username" in result_data or "text" in result_data or "content" in result_data:
                    posts = [result_data]
            elif isinstance(result_data, list):
                posts = result_data

            for post in posts[:max_items]:
                try:
                    # Extract data with various possible key names
                    formatted = {
                        "source": "x",
                        "content": (post.get("text") or
                                   post.get("content") or
                                   post.get("tweet_text") or
                                   post.get("full_text", "")),
                        "author": (post.get("username") or
                                  post.get("author") or
                                  post.get("user", {}).get("username", "")),
                        "author_name": (post.get("displayName") or
                                       post.get("name") or
                                       post.get("user", {}).get("name", "")),
                        "date": (post.get("created_at") or
                                post.get("timestamp") or
                                post.get("date", "")),
                        "url": (post.get("url") or
                               post.get("link") or
                               f"https://twitter.com/{post.get('username', 'user')}/status/{post.get('id', '')}"),
                        "engagement": {
                            "likes": (post.get("likes") or
                                     post.get("favorite_count") or
                                     post.get("like_count", 0)),
                            "retweets": (post.get("retweets") or
                                        post.get("retweet_count", 0)),
                            "replies": (post.get("replies") or
                                       post.get("reply_count", 0)),
                        },
                        "metadata": {
                            "id": post.get("id") or post.get("tweet_id", ""),
                            "language": post.get("lang") or post.get("language", ""),
                            "verified": post.get("verified", False),
                        }
                    }
                    results.append(formatted)
                except Exception as e:
                    self.logger.warning(f"⚠️  Failed to parse post: {e}")
                    continue

        except Exception as e:
            self.logger.error(f"❌ Error parsing X response: {e}")

        return results
