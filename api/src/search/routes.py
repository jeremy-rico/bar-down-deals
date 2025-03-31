from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.logging import get_logger
from src.deals.models import DealResponse
from src.search.models import SearchParams
from src.search.repository import SearchRepository
from src.search.service import SearchService

# Set up logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/search", tags=["search"])


def get_search_service(session: AsyncSession = Depends(get_session)) -> SearchService:
    """Dependency for getting search service instance."""
    repository = SearchRepository(session)
    return SearchService(repository)


@router.get("/", response_model=list[DealResponse])
async def search(
    response: Response,
    search_params: Annotated[SearchParams, Query()],
    service: SearchService = Depends(get_search_service),
) -> list[DealResponse]:
    """
    Search deals.

    Args:
        See src.search.models SearchParams
    """
    logger.debug("Searching deals")
    try:
        deals = await service.search(
            search_params.page,
            search_params.limit,
            search_params.q,
        )
        logger.info(f"Retrieved {len(deals[1])} deals")
        for k, i in deals[0].items():
            response.headers[k] = str(i)
        return deals[1]
    except Exception as e:
        logger.error(f"Failed to fetch deals: {str(e)}")
        raise
