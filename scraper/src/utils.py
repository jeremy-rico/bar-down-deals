import json
import logging
import re
import sys
from pathlib import Path

from scraper.src.settings import LOG_LEVEL, S3_HOST


def setup_logging() -> None:
    """Set up logging configuration."""
    format_string = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "CRITICAL": logging.CRITICAL,
    }
    logging.basicConfig(
        level=log_level_map[LOG_LEVEL],
        format=format_string,
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)


def clean_price(s: str) -> str | None:
    """
    Uses regular expression to find the first match of a floating point in the
    string

    Args:
        s: price string as scraped by spider

    Returns:
        str: re match
    """

    # re explanation:
    # \d: any number of digits
    # (,\d{3})?: optional comma and exactly three digits
    # .\d{2}: exactly decimal and two digits
    match = re.search(r"\d+(,\d{3})?\.\d{2}", s)
    if match:
        s = match.group(0)
        return "".join(s.split(",")) if "," in s else s


def clean_brand(s: str):
    """
    Clean scraped brand string
    """
    if s.lower().startswith("by"):
        return s.split()[-1]
    return s


def get_discount(salePrice: float, originalPrice: float | None) -> float | None:
    """
    Calculate discount
    """
    if not originalPrice:
        return None
    salePrice, originalPrice = float(salePrice), float(originalPrice)
    return (originalPrice - salePrice) / originalPrice * 100


def read_json(jsonPath: Path) -> dict:
    with open(str(jsonPath)) as f:
        return json.load(f)
