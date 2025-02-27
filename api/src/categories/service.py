from src.categories.models import CategoryResponse
from src.categories.repository import CategoryRepository


class CategoryService:
    """Service layer for category operations."""

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def get_categories(self) -> list[CategoryResponse]:
        """
        Get all categories.

        Returns:
            List[CategoryResponse]: List of all categories
        """
        categories = await self.repository.get_all()
        return [CategoryResponse.model_validate(category) for category in categories]

    async def get_category(self, category_id: int) -> CategoryResponse:
        """Get category by ID.

        Args:
            category_id: Category ID

        Returns:
            CategoryResponse: category data
        """
        category = await self.repository.get_by_id(category_id)
        return CategoryResponse.model_validate(category)
