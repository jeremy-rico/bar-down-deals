from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from api.core.config import settings

# Create declarative base for models
Base = declarative_base()


async def get_session() -> AsyncSession:
    """
    Dependency for getting async database session.

    Yields:
        AsyncSession: Async database session
    """
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

    # Create async session factory
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
