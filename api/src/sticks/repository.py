from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, func

from src.core.exceptions import NotFoundException
from src.core.logging import get_logger
from src.core.utils import convert_currency
from src.deals.models import Website
from src.sticks.models import (
    CurrentPrice,
    HistoricalPrice,
    Stick,
    StickImage,
    StickImageResponse,
    StickPrice,
)

logger = get_logger(__name__)


class StickRepository:
    """Repository for handling stick database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.granularity_map = {
            "1W": "day",
            "1M": "day",
            "6M": "week",
            "1Y": "month",
            "5Y": "month",
            "All": "day",  # NOTE: check this
        }

    async def get_all(
        self,
        sort: str,
        page: int,
        limit: int,
        brand: str | None,
        min_price: int | None,
        max_price: int | None,
        currency: str,
    ) -> list[Stick]:
        """
        Get all sticks.

        Returns:
            list of all sticks
        """
        # Create filters
        filters = []
        if brand:
            filters.append(Stick.brand == brand)
        if min_price:
            filters.append(Stick.price >= min_price)
        if max_price:
            filters.append(Stick.price <= max_price)

        # Main query
        stmt = select(Stick).filter(*filters).distinct()

        # Sorting
        if sort == "Oldest":
            stmt = stmt.order_by(col(Stick.created_at).asc())
        elif sort == "Newest":
            stmt = stmt.order_by(col(Stick.created_at).desc())
        elif sort == "Discount":
            stmt = stmt.where(col(Stick.discount) != None)
            stmt = stmt.order_by(col(Stick.discount).desc())
        elif sort == "Price Low":
            stmt = stmt.order_by(col(Stick.price).asc())
        elif sort == "Price High":
            stmt = stmt.order_by(col(Stick.price).desc())
        elif sort == "Alphabetical":
            stmt = stmt.order_by(col(Stick.model_name).asc())
        elif sort == "Random":
            stmt = stmt.order_by(func.random())

        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)

        # Convert currency
        sticks = list(result.scalars().all())
        for stick in sticks:
            stick.price = await convert_currency(self.session, stick.price, currency)
            if stick.msrp:
                stick.msrp = await convert_currency(self.session, stick.msrp, currency)

        return sticks

    async def get_by_id(self, stick_id: int, currency: str) -> Stick:
        """Get stick by ID.

        Args:
            stick_id: Stick ID
            currency: target currency

        Returns:
            Stick: Found stick

        Raises:
            NotFoundException: If stick not found
        """
        stmt = select(Stick).where(col(Stick.id) == stick_id)
        result = await self.session.execute(stmt)
        stick = result.scalar_one_or_none()

        if not stick:
            raise NotFoundException(f"Stick with id {stick_id} not found")

        stick.price = await convert_currency(self.session, stick.price, currency)
        stick.msrp = await convert_currency(self.session, stick.msrp, currency)

        return stick

    async def get_price_history(
        self, stick_id: int, since: str, currency: str
    ) -> list[HistoricalPrice]:
        """Get price history.

        Args:
            stick_id: Stick ID
            since: time window to grab from
            currency: target currency

        Returns:
            list of prices

        Raises:
            NotFoundException: If stick not found
        """
        since_map = {
            "1W": datetime.now(timezone.utc) - timedelta(weeks=1),
            "1M": datetime.now(timezone.utc) - timedelta(weeks=4),
            "6M": datetime.now(timezone.utc) - timedelta(weeks=4 * 6),
            "1Y": datetime.now(timezone.utc) - timedelta(days=365),
            "5Y": datetime.now(timezone.utc) - timedelta(days=365 * 5),
        }

        # Check if stick exists
        await self.get_by_id(stick_id, currency)

        truncation = self.granularity_map[since]

        stmt = (
            select(
                func.date_trunc(truncation, StickPrice.timestamp).label("trunc_time"),
                func.min(StickPrice.price).label("min_price"),
            )
            .where(col(StickPrice.stick_id) == stick_id)
            .group_by("trunc_time")
            .order_by("trunc_time")
        )

        if since in since_map:
            stmt = stmt.filter(col(StickPrice.timestamp) >= since_map[since])

        result = await self.session.execute(stmt)

        return [
            HistoricalPrice(
                timestamp=row[0],
                min_price=await convert_currency(self.session, row[1], currency),
            )
            for row in result.all()
        ]

    async def get_current_prices(
        self, stick_id: int, currency: str
    ) -> list[CurrentPrice]:
        """
        Get all prices for stick scraped in the last 24 hr
        """
        since = datetime.now(timezone.utc) - timedelta(days=1)
        stmt = (
            select(
                func.min(StickPrice.price).label("price"),
                col(StickPrice.currency),
                col(StickPrice.url),
                col(Website.name),
                col(Website.logo),
            )
            .join(Website)
            .where(
                col(StickPrice.stick_id) == stick_id, col(StickPrice.timestamp) >= since
            )
            .group_by(
                col(StickPrice.currency),
                col(StickPrice.url),
                col(Website.name),
                col(Website.logo),
            )
            .order_by("price")
        )
        result = await self.session.execute(stmt)
        return [
            CurrentPrice(
                price=await convert_currency(self.session, row[0], currency),
                currency=row[1],
                url=row[2],
                website_name=row[3],
                website_logo=row[4],
            )
            for row in result.all()
        ]

    async def get_images(self, stick_id) -> StickImageResponse:
        """
        Get images for one stick
        """
        stmt = (
            select(func.array_agg(col(StickImage.url)))
            .where(StickImage.stick_id == stick_id)
            .group_by(col(StickImage.stick_id))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_all_images(self) -> list[StickImageResponse]:
        """
        Bulk operation to get all images for each stick
        """
        stmt = select(
            col(StickImage.stick_id),
            func.array_agg(col(StickImage.url)).label("image_urls"),
        ).group_by(col(StickImage.stick_id))
        result = await self.session.execute(stmt)
        return [
            StickImageResponse(stick_id=row[0], image_urls=row[1])
            for row in result.all()
        ]
