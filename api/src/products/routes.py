from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.logging import get_logger
from src.products.models import FilterParams, ProductResponse, TagResponse
from src.products.repository import ProductRepository
from src.products.service import ProductService

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
    """
    Get products according to filter query.

    Args:
        See src.products.models FilterParams
    """
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


@router.get("/categories/", response_model=list[TagResponse])
async def get_categories(
    service: ProductService = Depends(get_product_service),
) -> list[TagResponse]:
    """
    Get all categories.

    Note: this route still uses the ProductService since categories are only
    assignable to products.
    """
    logger.debug("Fetching all categories")
    try:
        categories = await service.get_categories()
        logger.info(f"Retrieved {len(categories)} categories")
        return categories
    except Exception as e:
        logger.error(f"Failed to fetch categories: {str(e)}")
        raise
