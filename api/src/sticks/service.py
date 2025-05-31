from src.sticks.models import StickPriceResponse, StickResponse
from src.sticks.repository import StickRepository


class StickService:
    """Service layer for stick operations."""

    def __init__(self, repository: StickRepository):
        self.repository = repository

    async def get_sticks(
        self,
        sort: str,
        page: int,
        limit: int,
        brand: str | None,
        country: str | None,
        min_price: int,
        max_price: int | None,
    ) -> list[StickResponse]:
        """
        Get all sticks.

        Returns:
            List[StickResponse]: List of all sticks
        """
        sticks = await self.repository.get_all(
            sort=sort,
            page=page,
            limit=limit,
            brand=brand,
            country=country,
            min_price=min_price,
            max_price=max_price,
        )
        return [StickResponse.model_validate(stick) for stick in sticks]

    async def get_stick(self, stick_id: int) -> StickResponse:
        """Get stick by ID.

        Args:
            stick_id: Stick ID

        Returns:
            StickResponse: Stick data
        """
        stick = await self.repository.get_by_id(stick_id)
        return StickResponse.model_validate(stick)

    async def get_price_history(
        self, stick_id: int, time_period: str
    ) -> list[StickPriceResponse]:
        """
        Get historical price for stick ID

        Args:
            stick_id: stick id
            time_period: time period to grab prices

        Returns:
            list[StickPriceResponse]
        """
        prices = await self.repository.get_price_history(stick_id, time_period)
        return [StickPriceResponse.model_validate(price) for price in prices]
