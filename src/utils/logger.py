"""Logging configuration for Research Agent."""

import logging
import sys
from typing import Optional
from rich.logging import RichHandler
from src.config import Config


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name, defaults to 'research-agent'

    Returns:
        Configured logger instance
    """
    logger_name = name or "research-agent"
    logger = logging.getLogger(logger_name)

    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(getattr(logging, Config.LOG_LEVEL))

        # Use Rich handler for beautiful console output
        handler = RichHandler(
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            show_time=True,
            show_path=False,
        )

        formatter = logging.Formatter(
            "%(message)s",
            datefmt="[%X]"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.propagate = False

    return logger
