from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

# from api.src.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.logging import get_logger
from src.core.security import get_current_user
from src.products.models import FilterParams, ProductResponse
from src.products.repository import ProductRepository
from src.products.service import ProductService
from src.users.models import User

# Set up logger for this module
logger = get_logger(__name__)

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    """Dependency for getting product service instance."""
    repository = ProductRepository(session)
    return ProductService(repository)


@router.get("/", response_model=list[ProductResponse])
async def get_products(
    filter_query: Annotated[FilterParams, Query()],
    service: ProductService = Depends(get_product_service),
) -> list[ProductResponse]:
    """Get paginated products."""
    logger.debug("Fetching all products")
    try:
        products = await service.get_products(
            filter_query.sort_by,
            filter_query.page,
            filter_query.limit,
            filter_query.added_since,
        )
        logger.info(f"Retrieved {len(products)} products")
        return products
    except Exception as e:
        logger.error(f"Failed to fetch products: {str(e)}")
        raise


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
    # current_user: User = Depends(get_current_user),
) -> ProductResponse:
    """Get product by ID."""
    logger.debug(f"Fetching product {product_id}")
    try:
        product = await service.get_product(product_id)
        logger.info(f"Retrieved product {product_id}")
        return product
    except Exception as e:
        logger.error(f"Failed to fetch product {product_id}: {str(e)}")
        raise
