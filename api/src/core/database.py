from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import DATABASE_URL

# Create DB session connection ONCE
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    """
    Dependency for getting async database session.

    Yields:
        AsyncSession: Async database session
    """
    # Create async session factory
    async with async_session() as session:
        yield session
