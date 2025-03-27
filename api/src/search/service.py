from src.deals.models import DealResponse
from src.search.repository import SearchRepository


class SearchService:
    """Service layer for deal search."""

    def __init__(self, repository: SearchRepository):
        self.repository = repository

    async def search(
        self,
        page: int,
        limit: int,
        query: str,
    ) -> list[DealResponse]:
        """
        Get deals according to search.

        Returns:
            List[deal]: List of products
        """
        deals = await self.repository.search(page, limit, query)
        return [DealResponse.model_validate(deal) for deal in deals]
