import logging
import sys

from scrapers.site_scraper.src.settings import LOG_LEVEL


def setup_logging() -> None:
    """Set up logging configuration."""
    format_string = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    logging.getLogger("botocore").setLevel(LOG_LEVEL)
    logging.getLogger("urllib3").setLevel(LOG_LEVEL)
    logging.basicConfig(
        level=LOG_LEVEL,
        format=format_string,
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
