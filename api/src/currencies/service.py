from src.currencies.models import ExchangeRateResponse
from src.currencies.repository import ExchangeRateRepository


class ExchangeRateService:
    """Service layer for exchange rate operations."""

    def __init__(self, repository: ExchangeRateRepository):
        self.repository = repository

    async def get_rates(
        self,
    ) -> list[ExchangeRateResponse]:
        """
        Get all rates.

        Returns:
            List[ExchangeRateResponse]: List of all exchange rates
        """
        rates = await self.repository.get_all()
        return [ExchangeRateResponse.model_validate(rate) for rate in rates]
