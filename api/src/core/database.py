from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import DATABASE_URL

# Create DB session connection ONCE on app startup
# By default the session has a pool of 5 connections with a max limit of 10 and
# a pool timeout of 30s

# Each time a route is called, a connection in the pool is opened, queries are
# run, and then the connection is closed.
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session.

    Yields:
        AsyncSession: Async database session
    """
    # Create async session factory
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
