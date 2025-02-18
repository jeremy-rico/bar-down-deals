from fastapi import APIRouter, Depends, status

# from api.src.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.logging import get_logger
from src.core.security import get_current_user
from src.deals.models import Deal, DealResponse
from src.deals.repository import DealRepository
from src.deals.service import DealService
from src.users.models import User

# Set up logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/deals", tags=["deals"])


def get_deal_service(session: AsyncSession = Depends(get_session)) -> DealService:
    """Dependency for getting deal service instance."""
    repository = DealRepository(session)
    return DealService(repository)


@router.get("/", response_model=list[DealResponse])
async def get_all_deals(
    service: DealService = Depends(get_deal_service),
    # current_user: User = Depends(get_current_user),
) -> list[DealResponse]:
    """Get all deals."""
    logger.debug("Fetching all deals")
    try:
        deals = await service.get_all_deals()
        logger.info(f"Retrieved {len(deals)} deals")
        return deals
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


# @router.post("/", response_model=DealResponse, status_code=status.HTTP_201_CREATED)
# async def create_deal(
#     deal_data: DealCreate,
#     service: DealService = Depends(get_deal_service),
#     current_user: User = Depends(get_current_user),
# ) -> DealResponse:
#     """Create a new deal."""
#     logger.debug("Creating new deal")
#     try:
#         deal = await service.create_deal(deal_data)
#         logger.info(f"Created deal {deal.id}")
#         return deal
#     except Exception as e:
#         logger.error(f"Failed to create deal: {str(e)}")
#         raise


# @router.patch("/{deal_id}", response_model=DealResponse)
# async def update_deal(
#     deal_id: int,
#     deal_data: DealUpdate,
#     service: DealService = Depends(get_deal_service),
#     current_user: User = Depends(get_current_user),
# ) -> DealResponse:
#     """Update deal by ID."""
#     logger.debug(f"Updating deal {deal_id}")
#     try:
#         deal = await service.update_deal(deal_id, deal_data)
#         logger.info(f"Updated deal {deal_id}")
#         return deal
#     except Exception as e:
#         logger.error(f"Failed to update deal {deal_id}: {str(e)}")
#         raise
#
#
# @router.delete("/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_deal(
#     deal_id: int,
#     service: DealService = Depends(get_deal_service),
#     current_user: User = Depends(get_current_user),
# ) -> None:
#     """Delete deal by ID."""
#     logger.debug(f"Deleting deal {deal_id}")
#     try:
#         await service.delete_deal(deal_id)
#         logger.info(f"Deleted deal {deal_id}")
#     except Exception as e:
#         logger.error(f"Failed to delete deal {deal_id}: {str(e)}")
#         raise
