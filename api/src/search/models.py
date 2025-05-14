from typing import Literal

from pydantic import BaseModel
from sqlmodel import Field


# =========================== Search Parameter Model ====================
class SearchParams(BaseModel):
    """
    see /deals/models/QueryParams of parameter descriptions
    q: search query string
    """

    sort: Literal[
        "Popular",
        "Alphabetical",
        "Newest",
        "Oldest",
        "Discount",
        "Price High",
        "Price Low",
    ] = "Popular"
    page: int = Field(1, ge=1)
    limit: int = Field(20, gt=0, le=100)
    added_since: Literal["today", "week", "month", "year", "all"] = "all"
    country: Literal["US", "CA"] | None = Field(default=None)
    min_price: int = Field(0, ge=0)
    max_price: int | None = Field(default=None, ge=1)
    stores: list[str] | None = Field(default=None)
    brands: list[str] | None = Field(default=None)
    tags: list[str] | None = Field(default=None)
    q: str = Field(min_length=3, max_length=255)
