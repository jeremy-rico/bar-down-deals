from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import and_, col

from src.core.utils import get_headers
from src.deals.models import Deal
from src.products.models import Product


class SearchRepository:
    """Repository for handling deal search."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(
        self, page: int, limit: int, query: str
    ) -> tuple[dict[str, str], list[Deal]]:
        """
        Get products according to search.

        Args:
            search_string: search query

        Returns:
            List[Product]: List of products
        """
        stmt = select(Deal).join(Product)
        for kword in query.split():
            stmt = stmt.where(col(Product.name).ilike(f"%{kword}%"))

        # Get headers
        result = await self.session.execute(stmt)
        data = list(result.scalars().all())
        headers = get_headers(data, limit)

        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return headers, list(result.scalars().all())
