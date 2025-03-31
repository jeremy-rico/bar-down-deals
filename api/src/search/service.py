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
    ) -> tuple[dict[str, str], list[DealResponse]]:
        """
        Get deals according to search.

        Returns:
            List[deal]: List of products
        """
        headers, deals = await self.repository.search(page, limit, query)
        return headers, [DealResponse.model_validate(deal) for deal in deals]
