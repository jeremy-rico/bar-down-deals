import json
import math
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, func

from src.core.exceptions import AlreadyExistsException, NotFoundException
from src.core.utils import get_headers
from src.deals.models import Deal, Website
from src.products.models import Product, Tag, TagProductLink


class DealRepository:
    """Repository for handling Hero database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.timeframes = {
            "today": datetime.now(timezone.utc) - timedelta(days=1),
            "week": datetime.now(timezone.utc) - timedelta(weeks=1),
            "month": datetime.now(timezone.utc) - timedelta(weeks=4),
            "year": datetime.now(timezone.utc) - timedelta(days=365),
        }

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
    ) -> tuple[dict[str, str], list[Deal]]:
        """
        Get filtered deals.

        Returns:
            tuple(headers, List[Deal]): Custom headers, list of all deals
        """
        filters = []
        if min_price is not None:
            filters.append(Deal.price >= min_price)

        if max_price is not None:
            filters.append(Deal.price <= max_price)

        if stores:
            filters.append(col(Website.name).in_(stores))

        if brands:
            filters.append(col(Product.brand).in_(brands))

        if tags:
            filters.append(col(Tag.name).in_(tags))
            having_tag = func.count(col(Tag.name).distinct()) >= len(tags)
        else:
            having_tag = None

        if added_since in self.timeframes:
            filters.append(Deal.created_at >= self.timeframes[added_since])

        stmt = (
            select(Deal)
            .join(Website)
            .join(Product)
            .join(TagProductLink)
            .join(Tag)
            .group_by(col(Deal.id), Product.name)
            .filter(*filters)
            .distinct()
        )
        if having_tag is not None:
            stmt = stmt.having(having_tag)

        result = await self.session.execute(stmt)

        # TODO: sort by Popular
        if sort == "Oldest":
            stmt = stmt.order_by(col(Deal.created_at).asc())
        elif sort == "Newest":
            stmt = stmt.order_by(col(Deal.created_at).desc())
        elif sort == "Discount":
            stmt = stmt.order_by(col(Deal.discount).desc())
        elif sort == "Popular":
            stmt = stmt.order_by(col(Deal.views).desc())
        elif sort == "Price Low":
            stmt = stmt.order_by(col(Deal.price).asc())
        elif sort == "Price High":
            stmt = stmt.order_by(col(Deal.price).desc())
        elif sort == "Alphabetical":
            stmt = stmt.order_by(col(Product.name).asc())
        elif sort == "Random":
            stmt = stmt.order_by(func.random())

        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)

        # Get headers
        total_item_count = await self.get_item_count(filters)
        max_avail_price = await self.get_max_avail_price(
            added_since, min_price, stores, brands, tags
        )
        avail_brands = await self.get_available_brands(filters)
        avail_sizes, avail_tags = await self.get_available_sizes_and_tags(filters)
        avail_stores = await self.get_available_stores(filters)

        headers = {
            "x-total-item-count": total_item_count,
            "x-items-per-page": limit,
            "x-total-page-count": math.ceil(total_item_count / limit),
            "x-max-price": max_avail_price,
            "x-avail-sizes": json.dumps(avail_sizes),
            "x-avail-brands": json.dumps(avail_brands),
            "x-avail-tags": json.dumps(avail_tags),
            "x-avail-stores": json.dumps(avail_stores),
        }
        for k, v in headers.items():
            print(f"{k}: {v}")

        return headers, list(result.scalars().all())

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

        if not deal:
            raise NotFoundException(f"Deal with id {deal_id} not found")
        return deal

    async def increment_deal_by_id(self, deal_id: int) -> Deal:
        """
        Increment the amount of views a deal has by one.

        Args:
            deal_id: Deal ID

        Returns:
            Deal: incremented deal

        Raises:
            NotFoundException: If deal not found
        """
        stmt = select(Deal).where(col(Deal.id) == deal_id)
        result = await self.session.execute(stmt)
        deal = result.scalar_one_or_none()

        if not deal:
            raise NotFoundException(f"Deal with id {deal_id} not found")

        deal.views += 1
        self.session.add(deal)
        await self.session.commit()
        await self.session.refresh(deal)
        return deal

    async def get_item_count(self, filters: list) -> int:
        count_stmt = (
            select(func.count(col(Deal.id).distinct()))
            .join(Website)
            .join(Product)
            .join(TagProductLink)
            .join(Tag)
            .filter(*filters)
        )
        result = await self.session.execute(count_stmt)
        return result.scalars().one()

    async def get_max_avail_price(
        self,
        added_since: str,
        min_price: int | None,
        stores: list[str] | None,
        brands: list[str] | None,
        tags: list[str] | None,
    ):
        filters = []
        if min_price is not None:
            filters.append(Deal.price >= min_price)

        if stores:
            filters.append(col(Website.name).in_(stores))

        if brands:
            filters.append(col(Product.brand).in_(brands))

        if tags:
            filters.append(
                col(Tag.name).in_(tags)
                # .having(func.count(col(Tag.name).distinct()) >= len(tags))
            )

        if added_since in self.timeframes:
            filters.append(Deal.created_at >= self.timeframes[added_since])

        stmt = (
            select(func.max(col(Deal.price)))
            .join(Website)
            .join(Product)
            .join(TagProductLink)
            .join(Tag)
            .filter(*filters)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def get_available_brands(self, filters: list) -> list[str | None]:

        brand_stmt = (
            select(col(Product.brand))
            .join(Deal)
            .join(Website)
            .join(TagProductLink)
            .join(Tag)
            .filter(*filters)
            .distinct()
        )
        result = await self.session.execute(brand_stmt)
        return list(result.scalars().all())

    async def get_available_sizes_and_tags(
        self, filters: list
    ) -> tuple[list[str], list[str]]:

        sizes = ["Senior", "Intermediate", "Junior", "Youth", "Adult", "Womens"]

        tag_stmt = (
            select(col(Tag.name))
            .join(TagProductLink)
            .join(Product)
            .join(Deal)
            .join(Website)
            .filter(*filters)
            .distinct()
        )
        result = await self.session.execute(tag_stmt)
        avail_tags = list(result.scalars().all())
        avail_sizes = []
        for size in sizes:
            if size in avail_tags:
                avail_sizes.append(size)
                avail_tags.remove(size)
        return avail_sizes, avail_tags

    async def get_available_stores(self, filters: list) -> list[str]:
        store_stmt = (
            select(col(Website.name))
            .join(Deal)
            .join(Product)
            .join(TagProductLink)
            .join(Tag)
            .filter(*filters)
            .distinct()
        )
        result = await self.session.execute(store_stmt)
        return list(result.scalars().all())
