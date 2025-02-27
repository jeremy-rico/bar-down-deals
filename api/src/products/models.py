from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from src.categories.models import CategoryProductLink

if TYPE_CHECKING:
    from src.categories.models import Category, CategoryResponse
    from src.deals.models import Deal


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
            "brand={self.brand},created_at={self.created_at}, "
            "deals={self.deals},categories={self.categories})"
        )


class ProductResponse(ProductBase):
    id: int
    category: "CategoryResponse"


# =========================== Filter Query Parameter Model ====================
class FilterParams(BaseModel):
    sort_by: Literal["date"] = "date"
    page: int = Field(1, ge=1)
    limit: int = Field(20, gt=0, le=100)
    added_since: Literal["today", "week", "month", "year", "all"] = "all"
