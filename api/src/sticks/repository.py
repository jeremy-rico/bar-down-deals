import json
import math
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import and_, col, func, or_

from src.core.exceptions import NotFoundException
from src.core.logging import get_logger
from src.deals.models import Website
from src.sticks.models import Stick, StickPrice

logger = get_logger(__name__)


class StickRepository:
    """Repository for handling stick database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self,
        sort: str,
        page: int,
        limit: int,
        brand: str | None,
        country: str | None,
        min_price: int | None,
        max_price: int | None,
    ) -> list[Stick]:
        """
        Get all sticks.

        Returns:
            list of all sticks
        """
        stmt = (
            select(Stick)
            # .join(StickPrice)
            # .join(Website)
            # .filter(*filters)
        )

        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def get_by_id(self, stick_id: int) -> Stick:
        """Get stick by ID.

        Args:
            stick_id: Stick ID

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
        return stick

    async def get_price_history(
        self, stick_id: int, time_period: str
    ) -> list[StickPrice]:
        """Get price history.

        Args:
            stick_id: Stick ID
            time_period: time window to grab from

        Returns:
            list of prices

        Raises:
            NotFoundException: If stick not found
        """
        time_period_map = {
            "1W": datetime.now(timezone.utc) - timedelta(weeks=1),
            "1M": datetime.now(timezone.utc) - timedelta(weeks=4),
            "6M": datetime.now(timezone.utc) - timedelta(weeks=4 * 6),
            "1Y": datetime.now(timezone.utc) - timedelta(days=365),
            "5Y": datetime.now(timezone.utc) - timedelta(days=365 * 5),
        }

        # Check if stick exists
        await self.get_by_id(stick_id)

        stmt = select(StickPrice).where(col(StickPrice.stick_id) == stick_id)

        if time_period in time_period_map:
            start_date = time_period_map[time_period]
            stmt = stmt.filter(col(StickPrice.timestamp) >= start_date)

        result = await self.session.execute(stmt)

        return list(result.scalars().all())
