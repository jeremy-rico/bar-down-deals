from src.products.models import ProductResponse
from src.products.repository import ProductRepository


class ProductService:
    """Service layer for product operations."""

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def get_product(self, product_id: int) -> ProductResponse:
        """Get product by ID.

        Args:
            product_id: Product ID

        Returns:
            ProductResponse: Product data
        """
        product = await self.repository.get_by_id(product_id)
        return ProductResponse.model_validate(product)

    async def get_products(
        self, sort_by: str, page: int, limit: int, added_since: str
    ) -> list[ProductResponse]:
        """
        Get all products.

        Returns:
            List[ProductResponse]: List of all products
        """
        products = await self.repository.get_all(sort_by, page, limit, added_since)
        return [ProductResponse.model_validate(product) for product in products]
