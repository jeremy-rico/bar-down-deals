from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.products.models import Product


# ============================= Category Models =================================
class CategoryBase(SQLModel):
    name: str = Field(max_length=255, unique=True)


class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    parent_id: int | None = Field(foreign_key="category.id")

    products: list["Product"] = Relationship(back_populates="category")
    parent: Optional["Category"] = Relationship(
        back_populates="subcategories",
        sa_relationship_kwargs={"remote_side": "Category.id"},
    )
    subcategories: list["Category"] = Relationship(back_populates="parent")


class CategoryResponse(CategoryBase):
    id: int
    parent_id: int | None


# ============================= SubCategory Models =================================
# class SubCategoryBase(SQLModel):
#     name: str = Field(max_length=255)
#
#
# class SubCategory(SubCategoryBase, table=True):
#     __table_args__ = (UniqueConstraint("name", "category_id", name="name_cat_unique"),)
#
#     id: int | None = Field(default=None, primary_key=True)
#     category_id: int = Field(foreign_key="category.id", ondelete="CASCADE")
#
#     category: "Category" = Relationship(back_populates="subcategories")
#     products: list["Product"] = Relationship(back_populates="subcategory")
#
#
# class SubCategoryResponse(SubCategoryBase):
#     id: int
# category: "CategoryResponse"
