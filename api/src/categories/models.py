from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.products.models import Product


# ======================== Category Product Link Table =========================
class CategoryProductLink(SQLModel, table=True):
    category_id: int | None = Field(
        default=None, foreign_key="category.id", primary_key=True
    )
    product_id: int | None = Field(
        default=None, foreign_key="product.id", primary_key=True
    )


# ============================= Category Models =================================
class CategoryBase(SQLModel):
    name: str = Field(max_length=255, unique=True)


class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    products: list["Product"] = Relationship(
        back_populates="categories", link_model=CategoryProductLink
    )


class CategoryResponse(CategoryBase):
    id: int
