from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session


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
