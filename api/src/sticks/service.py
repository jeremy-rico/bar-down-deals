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

        if not sticks:
            return []

        # Fetch all current prices in one go
        current_prices = await self.repository.get_current_price_bulk()

        # Map stick_id -> price for fast lookup
        price_map = {price.stick_id: price.current_price for price in current_prices}

        # Attach prices and construct response
        sticks_response = []
        for stick in sticks:
            stick_data = stick.model_dump()
            stick_data["price"] = price_map.get(stick.id)
            sticks_response.append(StickResponse.model_validate(stick_data))

        return sticks_response

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
