import json
import math
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import and_, col, func, or_

from src.core.exceptions import NotFoundException
from src.core.logging import get_logger
from src.deals.models import Deal, Website
from src.products.models import Product, Tag, TagProductLink

logger = get_logger(__name__)


class DealRepository:
    """Repository for handling Hero database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.sizes = ["Senior", "Intermediate", "Junior", "Youth", "Adult", "Womens"]
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
        country: str | None,
        min_price: int | None,
        default_max_price: int | None,
        max_price: int | None,
        default_stores: list[str] | None,
        stores: list[str] | None,
        default_brands: list[str] | None,
        brands: list[str] | None,
        default_tags: list[str] | None,
        tags: list[str] | None,
    ) -> tuple[dict[str, str], list[Deal]]:
        """
        Get filtered deals.

        Returns:
            tuple(headers, List[Deal]): Custom headers, list of all deals
        """
        # Create various filters for grabbing available filters
        filter_kwargs = {
            "added_since": added_since,
            "country": country,
            "min_price": min_price,
            "default_max_price": default_max_price,
            "max_price": max_price,
            "default_stores": default_stores,
            "stores": stores,
            "default_brands": default_brands,
            "brands": brands,
            "default_tags": default_tags,
            "tags": tags,
        }
        filters = self.build_filters(**filter_kwargs)

        stmt = (
            select(Deal)
            .join(Website)
            .join(Product)
            .join(TagProductLink)
            .join(Tag)
            .group_by(col(Deal.id), Product.name)
            .filter(*filters)
        )

        total_item_count = await self.get_item_count(stmt)
        max_avail_price = await self.get_max_avail_price(**filter_kwargs)
        avail_brands = await self.get_avail_brands(**filter_kwargs)
        avail_sizes, avail_tags = await self.get_avail_sizes_and_tags(**filter_kwargs)
        avail_stores = await self.get_avail_stores(**filter_kwargs)

        if sort == "Oldest":
            stmt = stmt.order_by(col(Deal.created_at).asc())
        elif sort == "Newest":
            stmt = stmt.order_by(col(Deal.created_at).desc())
        elif sort == "Discount":
            stmt = stmt.where(col(Deal.discount) != None)
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

    def build_filters(
        self,
        added_since: str | None = None,
        country: str | None = None,
        min_price: int | None = None,
        default_max_price: int | None = None,
        max_price: int | None = None,
        default_stores: list[str] | None = None,
        stores: list[str] | None = None,
        default_brands: list[str] | None = None,
        brands: list[str] | None = None,
        default_tags: list[str] | None = None,
        tags: list[str] | None = None,
        exclude_fields: list[str] = [],
    ) -> list:
        """
        Builds a list of filters used to create a statment, all arguments are
        optional.

        Args:
            See get_all_deals()

        Returns:
            tuple: list[filters]
        """
        filters = []

        if added_since in self.timeframes:
            filters.append(Deal.created_at >= self.timeframes[added_since])

        if country:
            filters.append(Website.ships_to == country)

        if "min_price" not in exclude_fields:
            if min_price is not None:
                filters.append(Deal.price >= min_price)

        # If both default_max_price and max_price exist, we filter by
        # whichever is greater
        if default_max_price:
            filters.append(Deal.price <= default_max_price)
        if max_price and "max_price" not in exclude_fields:
            filters.append(Deal.price <= max_price)

        if default_stores:
            filters.append(col(Website.name).in_(default_stores))
        if stores and "stores" not in exclude_fields:
            filters.append(col(Website.name).in_(stores))

        if default_brands:
            filters.append(col(Product.brand).in_(default_brands))
        if brands and "brands" not in exclude_fields:
            filters.append(col(Product.brand).in_(brands))

        if default_tags and tags:
            filters.append(self.process_tags(default_tags + tags))
        elif default_tags:
            filters.append(self.process_tags(default_tags))
        elif tags and "tags" not in exclude_fields:
            filters.append(self.process_tags(tags))

        return filters

    def process_tags(self, tags: list[str]):
        """
        Defines logic for and vs or filtering. Size tags (Senior, Intermediate,
        Junior, etc.) are grouped with an or_ and combined with all other tags
        using an and_.

        Ex: Senior, Intermediate, Sticks. Will return (Senior OR Intermediate)
        AND (Sticks). Selecting all Sticks that are Senior or Intermediate.

        Args:
            tags: list of user selected tags

        Returns:
            sqlalchemy Boolean Clause: filters to be applied

        """
        # seperate tags into size and other tags
        size_tags = []
        other_tags = []
        for tag in tags:
            if tag in self.sizes:
                size_tags.append(tag)
            else:
                other_tags.append(tag)

        # Create filters using and + or logic
        if size_tags and other_tags:
            return and_(
                col(Product.tags).any(
                    or_(*(col(Tag.name) == tag for tag in size_tags))
                ),
                col(Product.tags).any(
                    or_(*(col(Tag.name) == tag for tag in other_tags))
                ),
            )
        else:
            return col(Tag.name).in_(tags)

    async def get_item_count(self, stmt) -> int:
        """
        Get total items count returned from statment (ignores pagination)

        Args:
            stmt: sqlalchemy statement before sorting and pagination

        Returns:
            int: total item count
        """
        count_stmt = select(func.count()).select_from(stmt)
        result = await self.session.execute(count_stmt)
        return result.scalars().one()

    async def get_max_avail_price(self, **filter_kwargs):
        """
        Get max available price (ignores user input max price filter)
        """
        filters = self.build_filters(**filter_kwargs, exclude_fields=["max_price"])
        stmt = (
            select(Deal)
            .join(Website)
            .join(Product)
            .join(TagProductLink)
            .join(Tag)
            .group_by(col(Deal.id), Product.name)
            .filter(*filters)
        )
        stmt = select(func.max(stmt.c.price))
        result = await self.session.execute(stmt)
        return result.scalars().one() or 0

    async def get_avail_brands(self, **filter_kwargs) -> list[str | None]:
        """
        Get available brands based on filters ignoring brand filters
        """
        filters = self.build_filters(**filter_kwargs, exclude_fields=["brands"])
        stmt = (
            select(col(Product.brand))
            .join(Deal)
            .join(Website)
            .join(TagProductLink)
            .join(Tag)
            .group_by(Product.brand)
            .filter(*filters)
            .filter(col(Product.brand).isnot(None))
            .order_by(col(Product.brand).asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_avail_sizes_and_tags(
        self, **filter_kwargs
    ) -> tuple[list[str], list[str]]:
        """
        Get available sizes and tags. With this setup, selecting a size filter
        does not change the tags filter. Possibly change that later.
        """
        if filter_kwargs["default_tags"] is not None:
            avail_tags = await self.get_associated_tags(filter_kwargs["default_tags"])
        else:
            filters = self.build_filters(**filter_kwargs, exclude_fields=["tags"])

            stmt = (
                select(col(Tag.name))
                .join(TagProductLink)
                .join(Product)
                .join(Deal)
                .join(Website)
                .group_by(Tag.name)
                .filter(*filters)
                .order_by(col(Tag.name).asc())
            )
            result = await self.session.execute(stmt)
            avail_tags = list(result.scalars().all())

        avail_sizes = []
        for size in self.sizes:
            if size in avail_tags:
                avail_sizes.append(size)
                avail_tags.remove(size)
        return avail_sizes, avail_tags

    async def get_associated_tags(self, tag_names: list[str]) -> list[str]:
        """
        Get all tags associated with the Products returned from the tag_names
        variable. This is used to gather default tags on page load.
        """
        ass_tags = []
        for tag_name in tag_names:
            # Get all products associated with tag_name
            product_ids_stmt = (
                select(col(TagProductLink.product_id))
                .join(Tag)
                .where(col(Tag.name) == tag_name)
                .distinct()
                .subquery()
            )

            # Accumulate all distince tags found in products from step 1
            associated_tags_stmt = (
                select(col(Tag.name))
                .join(TagProductLink)
                .where(col(TagProductLink.product_id).in_(select(product_ids_stmt)))
                .distinct()
                .order_by(col(Tag.name).asc())
            )

            result = await self.session.execute(associated_tags_stmt)
            ass_tags += list(result.scalars().all())
        return ass_tags

    async def get_avail_stores(self, **filter_kwargs) -> list[str]:
        """
        Get available stores based on the filters.
        """
        filters = self.build_filters(**filter_kwargs, exclude_fields=["stores"])
        stmt = (
            select(col(Website.name))
            .join(Deal)
            .join(Product)
            .join(TagProductLink)
            .join(Tag)
            .group_by(Website.name)
            .filter(*filters)
            .order_by(col(Website.name).asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
