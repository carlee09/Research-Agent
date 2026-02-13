"""Base collector class."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.utils.logger import get_logger


class BaseCollector(ABC):
    """Base class for data collectors."""

    def __init__(self, api_key: str, api_url: str):
        """
        Initialize collector.

        Args:
            api_key: API key for authentication
            api_url: Base API URL
        """
        self.api_key = api_key
        self.api_url = api_url
        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    def collect(self, topic: str, max_items: int = 20) -> List[Dict[str, Any]]:
        """
        Collect data for the given topic.

        Args:
            topic: Research topic
            max_items: Maximum number of items to collect

        Returns:
            List of collected data items
        """
        pass

    def _format_result(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format raw API data into standardized structure.

        Args:
            raw_data: Raw data from API

        Returns:
            Formatted data dictionary
        """
        return {
            "content": raw_data.get("content", ""),
            "author": raw_data.get("author", ""),
            "date": raw_data.get("date", ""),
            "url": raw_data.get("url", ""),
            "metadata": raw_data.get("metadata", {}),
        }
