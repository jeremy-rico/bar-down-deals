from fastapi import Depends
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.categories.models import Category
from src.core.config import settings
from src.core.database import get_session


async def populate_categories(
    categories: list[str],
    session: AsyncSession = Depends(get_session),
) -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        try:
            for category in categories:
                stmt = (
                    insert(Category)
                    .values(name=category)
                    .on_conflict_do_nothing(index_elements=["name"])
                    .returning(Category)
                )
                await session.execute(stmt)
                await session.commit()
            print("Categories populated.")

        except Exception as e:
            print(f"An error occurred while populating categories: {e}")

        await session.close()
