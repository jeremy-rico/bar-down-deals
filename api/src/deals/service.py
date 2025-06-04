from src.core.utils import convert_currency
from src.deals.models import DealResponse
from src.deals.repository import DealRepository


class DealService:
    """Service layer for deal operations."""

    def __init__(self, repository: DealRepository):
        self.repository = repository

    async def get_deals(
        self,
        sort: str,
        page: int,
        limit: int,
        added_since: str,
        country: str | None,
        min_price: int,
        default_max_price: int | None,
        max_price: int | None,
        default_stores: list[str] | None,
        stores: list[str] | None,
        default_brands: list[str] | None,
        brands: list[str] | None,
        default_tags: list[str] | None,
        tags: list[str] | None,
        currency: str,
    ) -> tuple[dict[str, str], list[DealResponse]]:
        """
        Get all deals.

        Returns:
            List[DealResponse]: List of all deals
        """
        headers, deals = await self.repository.get_all(
            sort=sort,
            page=page,
            limit=limit,
            added_since=added_since,
            country=country,
            min_price=min_price,
            default_max_price=default_max_price,
            max_price=max_price,
            default_stores=default_stores,
            stores=stores,
            default_brands=default_brands,
            brands=brands,
            default_tags=default_tags,
            tags=tags,
        )

        # Convert currency if necessary
        for deal in deals:
            if deal.currency != currency:
                deal.price = await convert_currency(deal.price, deal.currency, currency)
                if deal.original_price:
                    deal.original_price = await convert_currency(
                        deal.original_price, deal.currency, currency
                    )

        return headers, [DealResponse.model_validate(deal) for deal in deals]

    async def get_deal(self, deal_id: int, currency: str) -> DealResponse:
        """Get deal by ID.

        Args:
            deal_id: Deal ID

        Returns:
            DealResponse: Deal data
        """
        deal = await self.repository.get_by_id(deal_id)

        # Convert currency if necessary
        if deal.currency != currency:
            deal.price = await convert_currency(deal.price, deal.currency, currency)
            if deal.original_price:
                deal.original_price = await convert_currency(
                    deal.original_price, deal.currency, currency
                )

        return DealResponse.model_validate(deal)

    async def increment_deal(self, deal_id: int) -> DealResponse:
        """
        Incrememnt deal views by one

        """
        deal = await self.repository.increment_deal_by_id(deal_id)
        return DealResponse.model_validate(deal)
