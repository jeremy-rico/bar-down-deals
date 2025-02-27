from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.categories.models import Category


class CategoryRepository:
    """Repository for handling Hero database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Category]:
        """Get filtered categories.

        Returns:
            List[Category]: List of all categories
        """
        stmt = select(Category)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
