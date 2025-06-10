from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scrapers.stick_scraper.src.logging import get_logger
from scrapers.stick_scraper.src.settings import DATABASE_URL

logger = get_logger(__name__)


# Create engine
engine = create_engine(DATABASE_URL, echo=False, future=True)


def get_session() -> Session:
    """
    Dependency for getting database session.

    Yields:
        Session: Database session
    """

    # Create session
    return Session(engine)
