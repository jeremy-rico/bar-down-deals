from typing import Literal

from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    sort_by: Literal["last_scraped", "discount"] = "last_scraped"
    page: int = Field(1, ge=1)
    limit: int = Field(20, gt=0, le=100)
    added_since: Literal["today", "week", "month", "year", "all"] = "all"
