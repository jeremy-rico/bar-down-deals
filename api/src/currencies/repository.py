from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from src.core.config import settings
from src.currencies.models import ExchangeRate


class ExchangeRateRepository:
    """Repository for handling exchange rate base operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self,
    ) -> list[ExchangeRate]:
        """
        Get all rates.

        """
        stmt = (
            select(ExchangeRate)
            .where(col(ExchangeRate.target_currency).in_(settings.SUPPORTED_CURRENCIES))
            .order_by(ExchangeRate.target_currency)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
