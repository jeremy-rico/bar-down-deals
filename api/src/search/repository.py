from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from src.deals.models import Deal
from src.products.models import Product


class SearchRepository:
    """Repository for handling deal search."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(self, page: int, limit: int, query: str) -> list[Deal]:
        """
        Get products according to search.

        Args:
            search_string: search query

        Returns:
            List[Product]: List of products
        """
        stmt = select(Deal).join(Product).where(col(Product.name).ilike(f"%{query}%"))

        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
