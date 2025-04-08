import logging
from datetime import datetime, timedelta, timezone

from api.src.deals.models import Deal
from api.src.products.models import Product
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session
from sqlmodel import col, delete

logging.getLogger().setLevel(logging.INFO)


def get_session(database_url: URL) -> Session:
    """
    Dependency for getting database session.

    Yields:
        Session: Database session
    """
    # Create engine
    engine = create_engine(database_url, echo=False, future=True)

    # Create session
    return Session(engine)


def clean_database(database_url: URL) -> None:
    """
    After nightly scrape, remove deals that are over 48 hrs old. This means they
    haven't been scraped twice in a row and are probably removed from the parent
    site.

    """
    logging.info("Cleaning database...")
    session = get_session(database_url)
    expiration = datetime.now(timezone.utc) - timedelta(days=2)

    stmt = delete(Deal).filter(col(Deal.updated_at) <= expiration)

    try:
        session.execute(stmt)
        session.commit()
        logging.info("Successfully cleaned database.")
    except Exception as e:
        logging.critical(f"Failed to clean database: {e}")
        session.rollback()
