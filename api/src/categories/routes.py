from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.categories.models import CategoryResponse
from src.categories.repository import CategoryRepository
from src.categories.service import CategoryService
from src.core.database import get_session
from src.core.logging import get_logger

# Set up logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/categories", tags=["categories"])


def get_category_service(
    session: AsyncSession = Depends(get_session),
) -> CategoryService:
    """Dependency for getting category service instance."""
    repository = CategoryRepository(session)
    return CategoryService(repository)


@router.get("/", response_model=list[CategoryResponse])
async def get_categories(
    service: CategoryService = Depends(get_category_service),
) -> list[CategoryResponse]:
    """Get paginated categories."""
    logger.debug("Fetching all categories")
    try:
        categories = await service.get_categories()
        logger.info(f"Retrieved {len(categories)} categories")
        return categories
    except Exception as e:
        logger.error(f"Failed to fetch categories: {str(e)}")
        raise
