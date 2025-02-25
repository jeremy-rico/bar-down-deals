from src.deals.models import DealResponse
from src.deals.repository import DealRepository

# from src.deals.schemas import DealCreate, DealUpdate


class DealService:
    """Service layer for deal operations."""

    def __init__(self, repository: DealRepository):
        self.repository = repository

    # async def create_deal(self, deal_data: DealCreate) -> DealResponse:
    #     """Create a new deal.
    #
    #     Args:
    #         deal_data: Deal creation data
    #
    #     Returns:
    #         DealResponse: Created deal data
    #     """
    #     deal = await self.repository.create(deal_data)
    #     return DealResponse.model_validate(deal)
    #
    async def get_deal(self, deal_id: int) -> DealResponse:
        """Get deal by ID.

        Args:
            deal_id: Deal ID

        Returns:
            DealResponse: Deal data
        """
        deal = await self.repository.get_by_id(deal_id)
        return DealResponse.model_validate(deal)

    async def get_deals(
        self, sort_by: str, page: int, limit: int, added_since: str
    ) -> list[DealResponse]:
        """
        Get all deals.

        Returns:
            List[DealResponse]: List of all deals
        """
        deals = await self.repository.get_all(sort_by, page, limit, added_since)
        return [DealResponse.model_validate(deal) for deal in deals]

    # async def update_deal(self, deal_id: int, deal_data: DealUpdate) -> DealResponse:
    #     """Update deal by ID.
    #
    #     Args:
    #         deal_id: Deal ID
    #         deal_data: Deal update data
    #
    #     Returns:
    #         DealResponse: Updated deal data
    #     """
    #     deal = await self.repository.update(deal_id, deal_data)
    #     return DealResponse.model_validate(deal)
    #
    # async def delete_deal(self, deal_id: int) -> None:
    #     """Delete deal by ID.
    #
    #     Args:
    #         deal_id: Deal ID
    #     """
    #     await self.repository.delete(deal_id)
