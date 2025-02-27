import asyncio
import json
from pathlib import Path

from fastapi import Depends
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

from src.categories.models import Category
from src.core.config import settings
from src.core.database import get_session


async def populate_categories(session: AsyncSession = Depends(get_session)) -> None:
    jsonPath = Path(__file__).parent / "categories.json"
    with open(str(jsonPath)) as f:
        categories = json.load(f)

    engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        try:
            for category, subcategories in categories.items():
                stmt = (
                    insert(Category)
                    .values(name=category)
                    .on_conflict_do_nothing(index_elements=["name"])
                    .returning(Category)
                )
                result = await session.execute(stmt)
                await session.commit()
                cat = result.scalar()

                for subcategory in subcategories:
                    if not cat:
                        stmt = select(Category).where(Category.name == category)
                        result = await session.execute(stmt)
                        cat = result.scalar()

                    stmt = (
                        insert(Category)
                        .values(name=subcategory, parent_id=cat.id)
                        .on_conflict_do_nothing(index_elements=["name"])
                        .returning(Category)
                    )
                    await session.execute(stmt)
                    await session.commit()
        except Exception as e:
            print(f"An error occurred while populating categories: {e}")

        print("Categories populated.")
        await session.close()
