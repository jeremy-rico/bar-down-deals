from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.logging import get_logger
from src.currencies.models import ExchangeRateResponse
from src.currencies.repository import ExchangeRateRepository
from src.currencies.service import ExchangeRateService

# Set up logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/exchange_rates", tags=["Exchange Rates"])


def get_currency_service(
    session: AsyncSession = Depends(get_session),
) -> ExchangeRateService:
    """Dependency for getting currency service instance."""
    repository = ExchangeRateRepository(session)
    return ExchangeRateService(repository)


@router.get("/", response_model=list[ExchangeRateResponse])
async def get_exchange_rates(
    service: ExchangeRateService = Depends(get_currency_service),
) -> list[ExchangeRateResponse]:
    """
    Get all exchange_rates
    """
    logger.debug("Fetching all exchange_rates")
    try:
        exchange_rates = await service.get_rates()
        logger.info(f"Retrieved {len(exchange_rates)} currencies")
        return exchange_rates
    except Exception as e:
        logger.error(f"Failed to fetch exchange_rates: {str(e)}")
        raise
