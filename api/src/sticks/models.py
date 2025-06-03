from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.deals.models import Website, WebsiteResponse


# ============================== Stick Models ===================================
class StickBase(SQLModel):
    model_name: str = Field(max_length=255, index=True)
    brand: str | None = Field(max_length=64)
    line: str = Field(max_length=255)
    msrp: Decimal = Field(max_digits=10, decimal_places=2)
    price: Decimal = Field(
        max_digits=10,
        decimal_places=2,
    )
    currency: str = Field(max_length=3)
    discount: Decimal | None = Field(max_digits=4, decimal_places=2)
    price_drop: bool = Field()
    historical_low: bool = Field()
    description: str = Field()
    handedness: str = Field(max_length=16)
    flex: int = Field()
    curve: str = Field(max_length=16)
    size: str = Field(max_length=16)
    kickpoint: str = Field(max_length=16)
    release_year: int = Field()


class Stick(StickBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))

    price_history: list["StickPrice"] = Relationship(
        back_populates="stick",
        cascade_delete=True,
        # sa_relationship_kwargs={"lazy": "selectin"},
    )

    images: list["StickImage"] = Relationship(
        back_populates="stick",
        cascade_delete=True,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class StickCreate(StickBase):
    pass


class StickResponse(StickBase):
    id: int
    images: list[str]
    updated_at: datetime
    created_at: datetime


# =========================== Stick Images Models =============================
class StickImageBase(SQLModel):
    url: str = Field(max_length=255, unique=True)


class StickImage(StickImageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    stick_id: int = Field(foreign_key="stick.id", ondelete="CASCADE")

    stick: "Stick" = Relationship(
        back_populates="images", sa_relationship_kwargs={"lazy": "selectin"}
    )


class StickImageResponse(BaseModel):
    stick_id: int
    image_urls: list[str]


# =========================== Stick Price Models ==============================
class StickPriceBase(SQLModel):
    price: Decimal = Field(max_digits=10, decimal_places=2)
    currency: str = Field(max_length=3)
    timestamp: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    url: str = Field(max_length=255)


class StickPrice(StickPriceBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    website_id: int = Field(foreign_key="website.id", ondelete="CASCADE")
    stick_id: int = Field(foreign_key="stick.id", ondelete="CASCADE")

    website: "Website" = Relationship(
        back_populates="stick_price", sa_relationship_kwargs={"lazy": "selectin"}
    )
    stick: "Stick" = Relationship(
        back_populates="price_history", sa_relationship_kwargs={"lazy": "selectin"}
    )


class StickPriceCreate(StickPriceBase):
    pass


class StickPriceResponse(StickPriceBase):
    id: int
    website: "WebsiteResponse"


class HistoricalPrice(BaseModel):
    timestamp: datetime
    min_price: float


# =============================== Filter Query Model ==========================
class StickQueryParams(BaseModel):
    """
    Query parameter for sticks endpoint

    sort: option to sort results
    page: page number
    limit: limit items per request
    country: country that website ships to
    min_price: minimum price
    max_price: max price determined by user
    brand: brands filter defined by user
    """

    sort: Literal[
        "Alphabetical",
        "Newest",
        "Oldest",
        "Discount",
        "Price High",
        "Price Low",
        "Random",
    ] = "Alphabetical"
    page: int = Field(1, ge=1)
    limit: int = Field(20, gt=0, le=100)
    brand: str | None = Field(default=None)
    country: Literal["US", "CA"] | None = Field(default=None)
    min_price: int = Field(0, ge=0)
    max_price: int | None = Field(default=None, ge=1)


class PriceQueryParams(BaseModel):
    """
    Query parameter for sticks endpoint

    time_period: time period to grab from
    """

    time_period: Literal["1W", "1M", "6M", "1Y", "5Y", "All"] = "1M"
