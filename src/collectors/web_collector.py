"""Web search data collector using Sela Network API."""

from typing import List, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import quote_plus

from .base import BaseCollector
from src.config import Config


class WebCollector(BaseCollector):
    """Collector for web search data via Sela Network API."""

    def __init__(self):
        """Initialize Web collector with Sela Network API credentials."""
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
        Collect web search results for the given topic.

        Args:
            topic: Research topic
            max_items: Maximum number of results to collect

        Returns:
            List of collected web results
        """
        self.logger.info(f"🌐 Collecting web data for topic: '{topic}'")

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # Google Search - use search_parameters only (no URL)
            payload = {
                "scrapeType": "GOOGLE_SEARCH",
                "search_parameters": {
                    "engine": "google",
                    "q": topic,
                    "location": "United States",
                    "location_requested": "United States",
                    "google_domain": "google.com",
                    "hl": "en",
                    "gl": "us",
                    "device": "desktop"
                },
                "postCount": max_items,
                "timeoutMs": 120000  # 2 minutes
            }

            # Debug logging
            self.logger.debug(f"Request URL: {self.api_url}")
            self.logger.debug(f"Request payload: {payload}")

            response = self.session.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=180  # 3 minutes timeout (longer than timeoutMs)
            )

            # Log response for debugging
            self.logger.info(f"Response status: {response.status_code}")
            if response.status_code != 200:
                self.logger.error(f"Error response: {response.text}")

            response.raise_for_status()

            data = response.json()

            if not data.get("success"):
                self.logger.error(f"❌ API returned success=false: {data.get('message')}")
                return []

            results = self._parse_web_response(data, max_items)

            self.logger.info(f"✅ Collected {len(results)} web results")
            return results

        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Error collecting web data: {e}")
            return []

    def _parse_web_response(self, data: Dict[str, Any], max_items: int) -> List[Dict[str, Any]]:
        """
        Parse Sela Network Web API response.

        Args:
            data: Raw API response
            max_items: Maximum items to return

        Returns:
            List of formatted web results
        """
        results = []

        try:
            result_data = data.get("data", {}).get("result", {})

            # Handle different possible response structures
            items = []
            if isinstance(result_data, dict):
                # Look for common keys that contain search results
                items = (result_data.get("organic_results") or
                        result_data.get("news_results") or
                        result_data.get("results") or
                        result_data.get("items") or
                        result_data.get("articles", []))

                # If result is a single item
                if "title" in result_data or "link" in result_data:
                    items = [result_data]
            elif isinstance(result_data, list):
                items = result_data

            for item in items[:max_items]:
                try:
                    # Extract data with various possible key names
                    formatted = {
                        "source": "web",
                        "title": item.get("title") or item.get("headline") or "",
                        "content": item.get("snippet") or item.get("description") or item.get("summary") or "",
                        "url": item.get("link") or item.get("url") or "",
                        "author": item.get("source") or item.get("domain") or item.get("site_name") or "",
                        "date": item.get("date") or item.get("published_date") or item.get("timestamp", ""),
                        "metadata": {
                            "domain": item.get("domain") or item.get("displayed_link") or "",
                            "position": item.get("position", 0),
                            "thumbnail": item.get("thumbnail") or item.get("image", ""),
                        }
                    }
                    results.append(formatted)
                except Exception as e:
                    self.logger.warning(f"⚠️  Failed to parse web result: {e}")
                    continue

        except Exception as e:
            self.logger.error(f"❌ Error parsing web response: {e}")

        return results
