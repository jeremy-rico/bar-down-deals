from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.logging import get_logger
from src.deals.models import DealResponse, QueryParams, WebsiteResponse
from src.deals.repository import DealRepository
from src.deals.service import DealService
from src.products.models import ProductResponse, TagResponse

# Set up logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/deals", tags=["deals"])

# Rebuild model with late added dependencies
DealResponse.model_rebuild()


def get_deal_service(session: AsyncSession = Depends(get_session)) -> DealService:
    """Dependency for getting deal service instance."""
    repository = DealRepository(session)
    return DealService(repository)


@router.get("/", response_model=list[DealResponse])
async def get_deals(
    response: Response,
    query_params: Annotated[QueryParams, Query()],
    service: DealService = Depends(get_deal_service),
) -> list[DealResponse]:
    """Get sorted, filtered, paginated deals."""
    logger.debug("Fetching all deals")
    try:
        deals = await service.get_deals(
            query_params.sort,
            query_params.page,
            query_params.limit,
            query_params.added_since,
            query_params.min_price,
            query_params.max_price,
            query_params.stores,
            query_params.brands,
            query_params.tags,
        )
        logger.info(f"Retrieved {len(deals[1])} deals")
        for k, i in deals[0].items():
            response.headers[k] = str(i)
        return deals[1]
    except Exception as e:
        logger.error(f"Failed to fetch deals: {str(e)}")
        raise


@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(
    deal_id: int,
    service: DealService = Depends(get_deal_service),
    # current_user: User = Depends(get_current_user),
) -> DealResponse:
    """Get deal by ID."""
    logger.debug(f"Fetching deal {deal_id}")
    try:
        deal = await service.get_deal(deal_id)
        logger.info(f"Retrieved deal {deal_id}")
        return deal
    except Exception as e:
        logger.error(f"Failed to fetch deal {deal_id}: {str(e)}")
        raise


@router.put("/{deal_id}", response_model=DealResponse)
async def increment_deal(
    deal_id: int,
    service: DealService = Depends(get_deal_service),
) -> DealResponse:
    """Increment deal.views by one using ID"""
    logger.debug(f"Incrementing deal {deal_id} ")
    try:
        deal = await service.increment_deal(deal_id)
        logger.info(f"Successfully incremented deal {deal_id}")
        return deal
    except Exception as e:
        logger.error(f"Failed to increment deal {deal_id}: {str(e)}")
        raise
