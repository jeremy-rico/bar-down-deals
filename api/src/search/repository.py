from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, func

from src.deals.models import Deal, Website
from src.products.models import Product, Tag, TagProductLink


class SearchRepository:
    """Repository for handling deal search."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(
        self,
        sort: str,
        page: int,
        limit: int,
        added_since: str,
        min_price: int | None,
        max_price: int | None,
        stores: list[str] | None,
        brands: list[str] | None,
        tags: list[str] | None,
        query: str,
    ) -> tuple[dict[str, str], list[Deal]]:
        """
        Get products according to search.

        Args:
            search_string: search query

        Returns:
            List[Product]: List of products
        """
        stmt = (
            select(Deal)
            .join(Website)
            .join(Product)
            .join(TagProductLink)
            .join(Tag)
            .group_by(col(Deal.id), Product.name)
        )
        for kword in query.split():
            stmt = stmt.where(col(Product.name).ilike(f"%{kword}%"))

        # Filter by price range
        if min_price != None:
            stmt = stmt.where(col(Deal.price) >= min_price)
        if max_price:
            stmt = stmt.where(col(Deal.price) <= max_price)

        # Filter by stores:
        if stores:
            stmt = stmt.where(col(Website.name).in_(stores))

        # Filter by brands
        if brands:
            stmt = stmt.where(col(Product.brand).in_(brands))

        # Filter by tags
        if tags:
            stmt = stmt.where(col(Tag.name).in_(tags)).having(
                func.count(col(Tag.name).distinct()) >= len(tags)
            )

        if added_since:
            timeframes = {
                "today": datetime.now(timezone.utc) - timedelta(days=1),
                "week": datetime.now(timezone.utc) - timedelta(weeks=1),
                "month": datetime.now(timezone.utc) - timedelta(weeks=4),
                "year": datetime.now(timezone.utc) - timedelta(days=365),
            }
            if added_since in timeframes:
                stmt = stmt.filter(col(Deal.created_at) >= timeframes[added_since])

        # TODO: sort by best
        if sort == "Oldest":
            stmt = stmt.order_by(col(Deal.created_at).asc())
        elif sort == "Newest":
            stmt = stmt.order_by(col(Deal.created_at).desc())
        elif sort == "Discount" or sort == "Popular":
            stmt = stmt.order_by(col(Deal.discount).desc())
        elif sort == "Price Low":
            stmt = stmt.order_by(col(Deal.price).asc())
        elif sort == "Price High":
            stmt = stmt.order_by(col(Deal.price).desc())
        elif sort == "Alphabetical":
            stmt = stmt.order_by(col(Product.name).asc())

        # Get headers
        result = await self.session.execute(stmt)
        data = list(result.scalars().all())
        headers = get_headers(data, limit)

        # Paginate and return
        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return headers, list(result.scalars().all())
