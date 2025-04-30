from typing import TYPE_CHECKING

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.users.models import Users


# ============================== User Alerts Model ============================
class UserAlertBase(SQLModel):
    keyword: str = Field(max_length=255)


class UserAlert(UserAlertBase, table=True):
    """User keyword based alert"""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")

    user: "Users" = Relationship(
        back_populates="alerts", sa_relationship_kwargs={"lazy": "selectin"}
    )


class UserAlertCreate(UserAlertBase):
    user_id: int


class UserAlertResponse(UserAlertBase):
    id: int
    user_id: int


# =========================== Query Param Model ===============================
class QueryParams(BaseModel):
    """
    Query params for /alert

    kw: keyword, string keyword which to send alerts on
    """

    kw: str = Field(max_length=255)
