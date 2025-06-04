from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.logging import get_logger
from src.deals.models import WebsiteResponse  # Need for model rebuild
from src.sticks.models import (
    CurrentPrice,
    CurrentPricesQueryParams,
    HistoricalPrice,
    PriceHistoryQueryParams,
    StickPriceResponse,
    StickQueryParams,
    StickResponse,
    SticksQueryParams,
)
from src.sticks.repository import StickRepository
from src.sticks.service import StickService

# Resolve nested model forward references
StickPriceResponse.model_rebuild()

# Set up logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/sticks", tags=["sticks"])


def get_stick_service(session: AsyncSession = Depends(get_session)) -> StickService:
    """Dependency for getting stick service instance."""
    repository = StickRepository(session)
    return StickService(repository)


@router.get("/", response_model=list[StickResponse])
async def get_sticks(
    query_params: Annotated[SticksQueryParams, Query()],
    service: StickService = Depends(get_stick_service),
) -> list[StickResponse]:
    """Get all sticks."""
    logger.debug("Fetching all sticks")
    try:
        sticks = await service.get_sticks(
            sort=query_params.sort,
            page=query_params.page,
            limit=query_params.limit,
            brand=query_params.brand,
            min_price=query_params.min_price,
            max_price=query_params.max_price,
            currency=query_params.currency,
        )
        logger.info(f"Retrieved {len(sticks)} sticks")

        return sticks
    except Exception as e:
        logger.error(f"Failed to fetch sticks: {str(e)}")
        raise


@router.get("/{stick_id}", response_model=StickResponse)
async def get_stick(
    query_params: Annotated[StickQueryParams, Query()],
    stick_id: int,
    service: StickService = Depends(get_stick_service),
) -> StickResponse:
    """Get Stick by ID."""
    logger.debug(f"Fetching Stick {stick_id}")
    try:
        stick = await service.get_stick(
            stick_id=stick_id, currency=query_params.currency
        )
        logger.info(f"Retrieved stick {stick_id}")
        return stick
    except Exception as e:
        logger.error(f"Failed to fetch stick {stick_id}: {str(e)}")
        raise


@router.get("/{stick_id}/current_prices", response_model=list[CurrentPrice])
async def get_current_prices(
    query_params: Annotated[CurrentPricesQueryParams, Query()],
    stick_id: int,
    service: StickService = Depends(get_stick_service),
) -> list[CurrentPrice]:
    logger.debug(f"Fetching prices for stick {stick_id}")
    try:
        prices = await service.get_current_prices(
            stick_id=stick_id, currency=query_params.currency
        )
        logger.info(f"Retrieved {len(prices)} prices")
        return prices
    except Exception as e:
        logger.error(f"Failed to fetch prices for stick {stick_id}: {e}")
        raise


@router.get("/{stick_id}/price_history", response_model=list[HistoricalPrice])
async def get_price_history(
    query_params: Annotated[PriceHistoryQueryParams, Query()],
    stick_id: int,
    service: StickService = Depends(get_stick_service),
) -> list[HistoricalPrice]:
    logger.debug(f"Fetching prices for stick {stick_id}")
    try:
        prices = await service.get_price_history(
            stick_id=stick_id, since=query_params.since, currency=query_params.currency
        )
        logger.info(f"Retrieved {len(prices)} prices")
        return prices
    except Exception as e:
        logger.error(f"Failed to fetch prices for stick {stick_id}: {e}")
        raise
