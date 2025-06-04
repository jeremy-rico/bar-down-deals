import gc
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.database import get_session
from src.core.logging import get_logger
from src.deals.models import DealQueryParams, DealResponse, DealsQueryParams
from src.deals.repository import DealRepository
from src.deals.service import DealService

# Resolve nested model forward references
from src.products.models import ProductResponse  # Needed for model_rebuild

DealResponse.model_rebuild()

# Set up logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/deals", tags=["deals"])


def get_deal_service(session: AsyncSession = Depends(get_session)) -> DealService:
    """Dependency for getting deal service instance."""
    repository = DealRepository(session)
    return DealService(repository)


@router.get("/", response_model=list[DealResponse])
async def get_deals(
    response: Response,
    query_params: Annotated[DealsQueryParams, Query()],
    service: DealService = Depends(get_deal_service),
) -> list[DealResponse]:
    """Get sorted, filtered, paginated deals."""
    logger.debug("Fetching all deals")
    try:
        deals = await service.get_deals(
            sort=query_params.sort,
            page=query_params.page,
            limit=query_params.limit,
            added_since=query_params.added_since,
            country=query_params.country,
            min_price=query_params.min_price,
            default_max_price=query_params.default_max_price,
            max_price=query_params.max_price,
            default_stores=query_params.default_stores,
            stores=query_params.stores,
            default_brands=query_params.default_brands,
            brands=query_params.brands,
            default_tags=query_params.default_tags,
            tags=query_params.tags,
            currency=query_params.currency,
        )
        logger.info(f"Retrieved {len(deals[1])} deals")

        for k, i in deals[0].items():
            response.headers[k] = str(i)

        # TODO: See if this helps memory leak?
        logger.info("Collecting garbage...")
        gc.collect()
        return deals[1]
    except Exception as e:
        logger.error(f"Failed to fetch deals: {str(e)}")
        raise


@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(
    deal_id: int,
    query_params: Annotated[DealQueryParams, Query()],
    service: DealService = Depends(get_deal_service),
) -> DealResponse:
    """Get deal by ID."""
    logger.debug(f"Fetching deal {deal_id}")
    try:
        deal = await service.get_deal(deal_id=deal_id, currency=query_params.currency)
        logger.info(f"Retrieved deal {deal_id}")
        return deal
    except Exception as e:
        logger.error(f"Failed to fetch deal {deal_id}: {str(e)}")
        raise


@router.put("/{deal_id}/inc", response_model=DealResponse)
async def increment_deal(
    request: Request,
    deal_id: int,
    service: DealService = Depends(get_deal_service),
) -> DealResponse:
    """
    Increment deal.views by one using ID. Requires frontend secret key to use.
    """
    frontend_key = request.headers.get("X-Frontend-Key")
    if frontend_key != settings.FRONTEND_KEY:
        logger.error(
            f"Failed to increment deal {deal_id}: Got frontend key {frontend_key}"
        )
        raise HTTPException(status_code=403, detail="Forbidden")

    logger.debug(f"Incrementing deal {deal_id} ")
    try:
        deal = await service.increment_deal(deal_id)
        logger.info(f"Incremented deal {deal_id}")
        return deal
    except Exception as e:
        logger.error(f"Failed to increment deal {deal_id}: {str(e)}")
        raise
