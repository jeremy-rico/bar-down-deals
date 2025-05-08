from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.products.models import Product, ProductResponse


# ============================= Website Models ==================================
class WebsiteBase(SQLModel):
    name: str = Field(max_length=255)
    url: str = Field(unique=True)
    ships_to: str = Field(max_length=255)


class Website(WebsiteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))

    deals: list["Deal"] = Relationship(back_populates="website", cascade_delete=True)

    def __repr__(self) -> str:
        return f"Website(id={self.id}, name={self.name}, url={self.url})"


class WebsiteResponse(WebsiteBase):
    id: int


# ============================== Deal Models ===================================
class DealBase(SQLModel):
    price: Decimal = Field(max_digits=10, decimal_places=2)
    original_price: Decimal | None = Field(max_digits=10, decimal_places=2)
    discount: Decimal | None = Field(max_digits=4, decimal_places=2)
    url: str = Field(unique=True)
    views: int = Field(default=0)


class Deal(DealBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", ondelete="CASCADE")
    website_id: int = Field(foreign_key="website.id", ondelete="CASCADE")
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))

    product: "Product" = Relationship(
        back_populates="deals", sa_relationship_kwargs={"lazy": "selectin"}
    )
    website: "Website" = Relationship(
        back_populates="deals", sa_relationship_kwargs={"lazy": "selectin"}
    )


class DealCreate(DealBase):
    pass


class DealResponse(DealBase):
    id: int
    updated_at: datetime
    created_at: datetime
    product: "ProductResponse"
    website: "WebsiteResponse"


# =============================== Filter Query Model ==========================
class QueryParams(BaseModel):
    """
    Query parameter for deals endpoint

    sort: option to sort results
    page: page number
    limit: limit items per request
    added_since: time since item was first scraped
    country: country that website ships to
    min_price: minimum price
    default_max_price: max price determined by app page
    max_price: max price determined by user
    default_stores: stores filter defined by page
    stores: list of stores defined by user
    default_brands: brands filter defined by page
    brand: brands filter defined by user
    default_tags: tags defined by page
    tags: tags filter defined by user
    """

    sort: Literal[
        "Popular",
        "Alphabetical",
        "Newest",
        "Oldest",
        "Discount",
        "Price High",
        "Price Low",
        "Random",
    ] = "Popular"
    page: int = Field(1, ge=1)
    limit: int = Field(20, gt=0, le=100)
    added_since: Literal["today", "week", "month", "year", "all"] = "all"
    country: Literal["US", "CA"] | None = Field(default=None)
    min_price: int = Field(0, ge=0)
    default_max_price: int | None = Field(default=None, ge=1)
    max_price: int | None = Field(default=None, ge=1)
    default_stores: list[str] | None = Field(default=None)
    stores: list[str] | None = Field(default=None)
    default_brands: list[str] | None = Field(default=None)
    brands: list[str] | None = Field(default=None)
    default_tags: list[str] | None = Field(default=None)
    tags: list[str] | None = Field(default=None)
