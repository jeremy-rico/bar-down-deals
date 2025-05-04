import logging
import sys


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


logger = get_logger(__name__)
