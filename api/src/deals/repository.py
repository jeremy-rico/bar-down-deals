import json
import math
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, func

from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.deals.models import Deal, Website
from src.products.models import Category, CategoryProductLink, Product


class DealRepository:
    """Repository for handling Hero database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
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
    ) -> tuple[dict[str, int], list[Deal]]:
        """
        Get filtered deals.

        Returns:
            tuple(headers, List[Deal]): Custom headers, list of all deals
        """
        stmt = (
            select(Deal)
            .join(Website)
            .join(Product)
            .join(CategoryProductLink)
            .join(Category)
            .group_by(col(Deal.id), Product.name)
        )

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
            stmt = stmt.where(col(Category.name).in_(tags)).having(
                func.count(col(Category.name).distinct()) >= len(tags)
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
        elif sort == "Discount" or sort == "Best Selling":
            stmt = stmt.order_by(col(Deal.discount).desc())
        elif sort == "Price Low":
            stmt = stmt.order_by(col(Deal.price).asc())
        elif sort == "Price High":
            stmt = stmt.order_by(col(Deal.price).desc())
        elif sort == "Alphabetical":
            stmt = stmt.order_by(col(Product.name).asc())

        # Generate response headers
        result = await self.session.execute(stmt)
        data = list(result.scalars().all())
        avail_brands = set()
        avail_tags = set()
        avail_stores = set()
        avail_sizes = set()
        ret_max_price = 0.0
        sizes = ["Senior", "Intermediate", "Junior", "Youth", "Adult", "Womens"]
        for row in data:
            if row.product.brand:
                avail_brands.add(row.product.brand)
            if row.product.categories:
                for cat in row.product.categories:
                    if cat.name in sizes:
                        avail_sizes.add(cat.name)
                    else:
                        avail_tags.add(cat.name)
            if row.website.name:
                avail_stores.add(row.website.name)
            ret_max_price = max(ret_max_price, row.price)

        headers = {
            "x-total-item-count": len(data),
            "x-items-per-page": limit,
            "x-total-page-count": math.ceil(len(data) / limit),
            "x-avail-sizes": json.dumps(list(avail_sizes)),
            "x-avail-brands": json.dumps(list(avail_brands)),
            "x-avail-tags": json.dumps(list(avail_tags)),
            "x-avail-stores": json.dumps(list(avail_stores)),
            "x-max-price": ret_max_price,
        }

        # Paginate and return objects
        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return headers, list(result.scalars().all())

    # async def create(self, deal_data: DealCreate) -> Deal:
    #     """Create a new deal.
    #
    #     Args:
    #         deal_data: Deal creation data
    #
    #     Returns:
    #         Deal: Created deal
    #
    #     Raises:
    #         AlreadyExistsException: If deal with same alias already exists
    #     """
    #     deal = Deal(**deal_data.model_dump())
    #     try:
    #         self.session.add(deal)
    #         await self.session.commit()
    #         await self.session.refresh(deal)
    #         return deal
    #     except IntegrityError:
    #         await self.session.rollback()
    #         raise AlreadyExistsException(
    #             f"Deal with alias {deal_data.id} already exists"
    #         )
    #
    async def get_by_id(self, deal_id: int) -> Deal:
        """Get deal by ID.

        Args:
            deal_id: Deal ID

        Returns:
            Deal: Found deal

        Raises:
            NotFoundException: If deal not found
        """
        stmt = select(Deal).where(col(Deal.id) == deal_id)
        result = await self.session.execute(stmt)
        deal = result.scalar_one_or_none()
        # deal = result.scalar.first()

        if not deal:
            raise NotFoundException(f"Deal with id {deal_id} not found")
        return deal

    # async def update(self, deal_id: int, deal_data: DealUpdate) -> Deal:
    #     """Update deal by ID.
    #
    #     Args:
    #         deal_id: Deal ID
    #         deal_data: Deal update data
    #
    #     Returns:
    #         Deal: Updated deal
    #
    #     Raises:
    #         NotFoundException: If deal not found
    #     """
    #     update_data = deal_data.model_dump(exclude_unset=True)
    #     if not update_data:
    #         raise ValueError("No fields to update")
    #
    #     query = update(Deal).where(Deal.id == deal_id).values(**update_data)
    #     result = await self.session.execute(query)
    #
    #     if result.rowcount == 0:
    #         raise NotFoundException(f"Deal with id {deal_id} not found")
    #
    #     await self.session.commit()
    #     return await self.get_by_id(deal_id)
    #
    # async def delete(self, deal_id: int) -> None:
    #     """Delete deal by ID.
    #
    #     Args:
    #         deal_id: Deal ID
    #
    #     Raises:
    #         NotFoundException: If deal not found
    #     """
    #     query = delete(Deal).where(Deal.id == deal_id)
    #     result = await self.session.execute(query)
    #
    #     if result.rowcount == 0:
    #         raise NotFoundException(f"Deal with id {deal_id} not found")
    #
