"""Input validation utilities."""

from typing import List
import click


def validate_topic(topic: str) -> str:
    """
    Validate research topic.

    Args:
        topic: Research topic string

    Returns:
        Validated topic string

    Raises:
        click.BadParameter: If topic is invalid
    """
    if not topic or not topic.strip():
        raise click.BadParameter("Topic cannot be empty")

    if len(topic.strip()) < 3:
        raise click.BadParameter("Topic must be at least 3 characters long")

    if len(topic) > 200:
        raise click.BadParameter("Topic must be less than 200 characters")

    return topic.strip()


def validate_sources(sources: str) -> List[str]:
    """
    Validate and parse data sources.

    Args:
        sources: Comma-separated list of sources (x, web, all)

    Returns:
        List of validated source names

    Raises:
        click.BadParameter: If sources are invalid
    """
    valid_sources = {"x", "web", "all"}

    if sources == "all":
        return ["x", "web"]

    source_list = [s.strip().lower() for s in sources.split(",")]

    for source in source_list:
        if source not in valid_sources:
            raise click.BadParameter(
                f"Invalid source '{source}'. Valid sources: x, web, all"
            )

    if "all" in source_list:
        return ["x", "web"]

    return list(set(source_list))  # Remove duplicates


def validate_depth(depth: str) -> str:
    """
    Validate analysis depth.

    Args:
        depth: Analysis depth (quick or detailed)

    Returns:
        Validated depth string

    Raises:
        click.BadParameter: If depth is invalid
    """
    valid_depths = {"quick", "detailed"}
    depth_lower = depth.lower()

    if depth_lower not in valid_depths:
        raise click.BadParameter(
            f"Invalid depth '{depth}'. Valid options: quick, detailed"
        )

    return depth_lower


def validate_max_items(max_items: int) -> int:
    """
    Validate maximum items count.

    Args:
        max_items: Maximum number of items to collect

    Returns:
        Validated max_items

    Raises:
        click.BadParameter: If max_items is invalid
    """
    if max_items < 1:
        raise click.BadParameter("max-items must be at least 1")

    if max_items > 100:
        raise click.BadParameter("max-items must be less than or equal to 100")

    return max_items
