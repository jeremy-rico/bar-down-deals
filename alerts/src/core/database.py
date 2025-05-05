from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from alerts.src.core.config import DATABASE_URL

# Create engine
engine = create_engine(DATABASE_URL, echo=False, future=True)


def get_session() -> Session:
    """
    Dependency for getting database session.

    Returns:
        Session: Database session
    """

    # Create session
    return Session(engine)
