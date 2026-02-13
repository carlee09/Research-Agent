"""Configuration management for Research Agent."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""

    # API Keys
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    SELA_API_KEY: str = os.getenv("SELA_API_KEY", "")
    SELA_API_ENDPOINT: str = os.getenv("SELA_API_ENDPOINT", "https://api.selanetwork.io/api/rpc/scrapeUrl")
    SELA_TIMEOUT_MS: int = int(os.getenv("SELA_TIMEOUT_MS", "60000"))

    # AI Model settings
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gemini")  # claude or gemini

    # Claude settings
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    CLAUDE_MAX_TOKENS: int = 4096
    CLAUDE_TEMPERATURE: float = 0.7

    # Gemini settings
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_MAX_TOKENS: int = 8192
    GEMINI_TEMPERATURE: float = 0.7

    # Collection settings
    DEFAULT_MAX_ITEMS: int = 20
    DEFAULT_SOURCES: str = "all"  # x, web, all
    DEFAULT_DEPTH: str = "detailed"  # quick, detailed

    # API settings
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2  # seconds
    REQUEST_TIMEOUT: int = 30  # seconds

    # Output settings
    OUTPUT_DIR: Path = Path(os.getenv("OUTPUT_DIR", "./reports"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls, model: str = None) -> bool:
        """Validate required configuration."""
        # Check if at least one AI API key is available
        if not cls.ANTHROPIC_API_KEY and not cls.GEMINI_API_KEY:
            raise ValueError("Either ANTHROPIC_API_KEY or GEMINI_API_KEY is required in .env file")

        # Check specific model key if specified
        if model == "claude" and not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required for Claude model")
        if model == "gemini" and not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required for Gemini model")

        if not cls.SELA_API_KEY:
            raise ValueError("SELA_API_KEY is required in .env file")
        return True

    @classmethod
    def ensure_output_dir(cls) -> None:
        """Ensure output directory exists."""
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Validate config on import (basic check)
try:
    if not Config.ANTHROPIC_API_KEY and not Config.GEMINI_API_KEY:
        print(f"⚠️  Configuration Warning: At least one AI API key (ANTHROPIC_API_KEY or GEMINI_API_KEY) is required")
        print("Please copy .env.example to .env and fill in your API keys.")
except Exception as e:
    print(f"⚠️  Configuration Error: {e}")
