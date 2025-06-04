from src.core.utils import convert_currency
from src.sticks.models import CurrentPrice, HistoricalPrice, StickResponse
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
        min_price: int,
        max_price: int | None,
        currency: str,
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
            min_price=min_price,
            max_price=max_price,
        )

        if not sticks:
            return []

        images = await self.repository.get_all_images()

        image_map = {image.stick_id: image.image_urls for image in images}

        # Attach prices and construct response
        sticks_response = []
        for stick in sticks:
            # Convert currency if necessary
            if stick.currency != currency:
                stick.price = convert_currency(stick.price, stick.currency, currency)
                if stick.msrp:
                    stick.msrp = convert_currency(stick.msrp, stick.currency, currency)

            # Get images
            stick_data = stick.model_dump()
            stick_data["images"] = image_map.get(stick.id)
            sticks_response.append(StickResponse.model_validate(stick_data))

        return sticks_response

    async def get_stick(self, stick_id: int, currency: str) -> StickResponse:
        """Get stick by ID.

        Args:
            stick_id: Stick ID

        Returns:
            StickResponse: Stick data
        """
        stick = await self.repository.get_by_id(stick_id)
        images = await self.repository.get_images(stick_id)
        stick_data = stick.model_dump()
        stick_data["images"] = images

        if stick.currency != currency:
            stick.price = convert_currency(stick.price, stick.currency, currency)
            if stick.msrp:
                stick.msrp = convert_currency(stick.msrp, stick.currency, currency)

        return StickResponse.model_validate(stick_data)

    async def get_current_prices(
        self, stick_id: int, currency: str
    ) -> list[CurrentPrice]:
        """
        Get prices from all stores for stick scraped in the past 24hrs
        """
        prices = await self.repository.get_current_prices(stick_id)

        for price in prices:
            if price.currency != currency:
                price.price = convert_currency(price.price, price.currency, currency)

        return [CurrentPrice.model_validate(price) for price in prices]

    async def get_price_history(
        self, stick_id: int, since: str, currency: str
    ) -> list[HistoricalPrice]:
        """
        Get historical price for stick ID

        Args:
            stick_id: stick id
            since: time period to grab prices

        Returns:
            list[StickPriceResponse]
        """
        prices = await self.repository.get_price_history(stick_id, since)
        return prices
