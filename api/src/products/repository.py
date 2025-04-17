from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from src.core.exceptions import NotFoundException
from src.products.models import Product, Tag


class ProductRepository:
    """Repository for handling Hero database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self, sort_by: str, page: int, limit: int, added_since
    ) -> list[Product]:
        """
        Get filtered products.

        Args:
            sort_by:
        Returns:
            List[Product]: List of all products
        """
        stmt = select(Product)
        if added_since:
            timeframes = {
                "today": datetime.now(timezone.utc) - timedelta(days=1),
                "week": datetime.now(timezone.utc) - timedelta(weeks=1),
                "month": datetime.now(timezone.utc) - timedelta(weeks=4),
                "year": datetime.now(timezone.utc) - timedelta(days=365),
            }
            if added_since in timeframes:
                stmt = stmt.filter(col(Product.created_at) >= timeframes[added_since])

        if sort_by == "date":
            stmt = stmt.order_by(col(Product.created_at))

        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_all_tags(self) -> list[Tag]:
        stmt = select(Tag)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, product_id: int) -> Product:
        """Get product by ID.

        Args:
            product_id: Product ID

        Returns:
            Product: Found product

        Raises:
            NotFoundException: If product not found
        """
        stmt = select(Product).where(col(Product.id) == product_id)
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            raise NotFoundException(f"Product with id {product_id} not found")
        return product
