from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Literal, Optional

from pydantic import BaseModel
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.products.models import Product, ProductResponse


# ============================= Website Models ==================================
class WebsiteBase(SQLModel):
    name: str = Field(max_length=255)
    url: str = Field(unique=True)


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
class FilterParams(BaseModel):
    sort: Literal["best", "alphabetical", "date", "discount", "price" ] = "date"
    order: Literal["asc", "desc"] = "desc"
    page: int = Field(1, ge=1)
    limit: int = Field(20, gt=0, le=100)
    added_since: Literal["today", "week", "month", "year", "all"] = "all"
    categories: list[int] | None = Field(default=None)
