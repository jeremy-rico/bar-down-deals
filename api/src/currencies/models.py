from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


# ======================== Exchange Rate Table =========================
class ExchangeRate(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    base_currency: str = Field(max_length=3)
    target_currency: str = Field(max_length=3, unique=True)
    rate: Decimal = Field()
    timestamp: datetime


class ExchangeRateResponse(SQLModel):
    base_currency: str = Field(max_length=3)
    target_currency: str = Field(max_length=3, unique=True)
    rate: Decimal = Field()


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
