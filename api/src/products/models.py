from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.deals.models import Deal


# ======================== Tag Product Link Table =========================
class TagProductLink(SQLModel, table=True):
    tag_id: int | None = Field(
        default=None, foreign_key="tag.id", primary_key=True, ondelete="CASCADE"
    )
    product_id: int | None = Field(
        default=None, foreign_key="product.id", primary_key=True, ondelete="CASCADE"
    )


# ============================= Tag Models =================================
class TagBase(SQLModel):
    name: str = Field(max_length=255, unique=True)


class Tag(TagBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    products: list["Product"] = Relationship(
        back_populates="tags", link_model=TagProductLink
    )


class TagResponse(TagBase):
    id: int


# ============================= Product Models =================================
class ProductBase(SQLModel):
    # TODO: Find a better way of avoiding duplicate products
    name: str = Field(max_length=255, index=True, unique=True)
    brand: str | None = Field(max_length=255)
    image_url: str | None


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))

    deals: list["Deal"] = Relationship(back_populates="product", cascade_delete=True)
    tags: list["Tag"] = Relationship(
        back_populates="products",
        link_model=TagProductLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self) -> str:
        return (
            f"Product(id={self.id}, name={self.name}, "
            f"brand={self.brand}, created_at={self.created_at}, "
            f"deals={self.deals}, tags={self.tags})"
        )


class ProductResponse(ProductBase):
    id: int
    tags: list["TagResponse"]


class ProductIDResponse(ProductBase):
    id: int
    description: str | None


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


# ============================= Brand Models ==================================
class BrandBase(SQLModel):
    name: str


class Brand(BrandBase):
    pass


class BrandResponse(BrandBase):
    pass
