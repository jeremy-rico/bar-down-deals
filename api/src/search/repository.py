import json
import math

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, func

from src.core.config import TAGS
from src.deals.models import Deal, Website
from src.products.models import Product, Tag, TagProductLink


class SearchRepository:
    """Repository for handling deal search."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(
        self,
        q: str,
        sort: str,
        page: int,
        limit: int,
        min_price: int | None,
        max_price: int | None,
        stores: list[str] | None,
        brands: list[str] | None,
        tags: list[str] | None,
    ) -> tuple[dict[str, str], list[Deal]]:
        """
        Get products according to search. Attempts to exact match each word in
        the search query.

        Args:
            q: search query
            see search/models.py searchParams

        Returns:
            dict, List[Deal]: tuple(headers, list of products)
        """
        filter_kwargs = {
            "q": q,
            "min_price": min_price,
            "max_price": max_price,
            "stores": stores,
            "brands": brands,
            "tags": tags,
        }
        filters = self.build_filters(**filter_kwargs)

        # Need to add a having statment if we're filtering by tags
        if tags:
            having_tag = func.count(col(Tag.name).distinct()) >= len(tags)
        else:
            having_tag = None

        stmt = (
            select(Deal)
            .join(Website)
            .join(Product)
            .join(TagProductLink)
            .join(Tag)
            .group_by(col(Deal.id), Product.name)
            .filter(*filters)
        )

        if having_tag is not None:
            stmt = stmt.having(having_tag)

        # Perform keyword search
        # for kword in q.split():
        #     stmt = stmt.where(col(Product.name).ilike(f"%{kword}%"))

        total_item_count = await self.get_item_count(stmt)
        max_avail_price = await self.get_max_avail_price(having_tag, **filter_kwargs)
        avail_brands = await self.get_avail_brands(having_tag, **filter_kwargs)
        avail_sizes, avail_tags = await self.get_avail_sizes_and_tags(**filter_kwargs)
        avail_stores = await self.get_avail_stores(having_tag, **filter_kwargs)

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

        # Paginate and return
        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return headers, list(result.scalars().all())

    def build_filters(
        self,
        q: str,
        min_price: int | None = None,
        max_price: int | None = None,
        stores: list[str] | None = None,
        brands: list[str] | None = None,
        tags: list[str] | None = None,
        exclude_fields: list[str] = [],
    ) -> list:
        """
        Builds a list of filters used to create a statment, all arguments are
        optional.

        Args:
            See search()

        Returns:
            list[filters]
        """
        filters = []
        if min_price and "min_price" not in exclude_fields:
            filters.append(Deal.price >= min_price)

        if max_price and "max_price" not in exclude_fields:
            filters.append(Deal.price <= max_price)

        if stores and "stores" not in exclude_fields:
            filters.append(col(Website.name).in_(stores))

        if brands and "brands" not in exclude_fields:
            filters.append(col(Product.brand).in_(brands))

        if tags and "tags" not in exclude_fields:
            filters.append(col(Tag.name).in_(tags))

        if len(q.split()) == 1 and q.title() in TAGS:
            filters.append(col(Tag.name) == q.title())
        else:
            for kword in q.split():
                filters.append(col(Product.name).ilike(f"%{kword}%"))

        return filters

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

    async def get_max_avail_price(self, having_tag, **filter_kwargs) -> int:
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
        if having_tag is not None:
            stmt = stmt.having(having_tag)
        stmt = select(func.max(stmt.c.price))
        result = await self.session.execute(stmt)
        return result.scalars().one() or 0

    async def get_avail_brands(self, having_tag, **filter_kwargs) -> list[str | None]:
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
        )
        if having_tag is not None:
            stmt = stmt.having(having_tag)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_avail_sizes_and_tags(
        self, **filter_kwargs
    ) -> tuple[list[str], list[str]]:
        """
        Get available sizes and tags. With this setup, selecting a size filter
        does not change the tags filter. Possibly change that later.
        """
        sizes = ["Senior", "Intermediate", "Junior", "Youth", "Adult", "Womens"]
        filters = self.build_filters(**filter_kwargs, exclude_fields=["tags"])
        stmt = (
            select(col(Tag.name))
            .join(TagProductLink)
            .join(Product)
            .join(Deal)
            .join(Website)
            .group_by(Tag.name)
            .filter(*filters)
        )
        result = await self.session.execute(stmt)
        avail_tags = list(result.scalars().all())

        avail_sizes = []
        for size in sizes:
            if size in avail_tags:
                avail_sizes.append(size)
                avail_tags.remove(size)
        return avail_sizes, avail_tags

    async def get_avail_stores(self, having_tag, **filter_kwargs) -> list[str]:
        filters = self.build_filters(**filter_kwargs, exclude_fields=["stores"])
        stmt = (
            select(col(Website.name))
            .join(Deal)
            .join(Product)
            .join(TagProductLink)
            .join(Tag)
            .group_by(Website.name)
            .filter(*filters)
        )
        if having_tag is not None:
            stmt = stmt.having(having_tag)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
