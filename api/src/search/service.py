from src.deals.models import DealResponse
from src.search.repository import SearchRepository


class SearchService:
    """Service layer for deal search."""

    def __init__(self, repository: SearchRepository):
        self.repository = repository

    async def search(
        self,
        sort: str,
        page: int,
        limit: int,
        added_since: str,
        min_price: int | None,
        max_price: int | None,
        stores: list[str] | None,
        brands: list[str] | None,
        tags: list[str] | None,
        query: str,
    ) -> tuple[dict[str, str], list[DealResponse]]:
        """
        Get deals according to search.

        Returns:
            List[deal]: List of products
        """
        headers, deals = await self.repository.search(
            sort=sort,
            page=page,
            limit=limit,
            added_since=added_since,
            min_price=min_price,
            max_price=max_price,
            stores=stores,
            brands=brands,
            tags=tags,
            query=query,
        )
        return headers, [DealResponse.model_validate(deal) for deal in deals]
