from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.deals.models import Deal


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


# ============================= Product Models =================================
class ProductBase(SQLModel):
    # TODO: Find a better way of avoiding duplicate products
    name: str = Field(max_length=255, index=True, unique=True)
    brand: str | None = Field(max_length=255)
    image_url: str | None
    description: str | None


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))

    deals: list["Deal"] = Relationship(back_populates="product", cascade_delete=True)
    categories: list["Category"] = Relationship(
        back_populates="products", link_model=CategoryProductLink
    )

    def __repr__(self) -> str:
        return (
            f"Product(id={self.id}, name={self.name}, "
            f"brand={self.brand},created_at={self.created_at}, "
            f"deals={self.deals},categories={self.categories})"
        )


class ProductResponse(ProductBase):
    id: int
    category: "CategoryResponse"


# =========================== Filter Query Parameter Model ====================
class FilterParams(BaseModel):
    """
    sort_by: how to sort response
    page: pagination
    limit: max items per response
    added_since: timeframe since item was added to db
    """

    sort_by: Literal["date"] = "date"
    page: int = Field(1, ge=1)
    limit: int = Field(20, gt=0, le=100)
    added_since: Literal["today", "week", "month", "year", "all"] = "all"
