from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, model_validator
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.users.models import Users


# ============================== User Alerts Model ============================
class UserAlertBase(SQLModel):
    size: str | None = Field(max_length=255, default=None)
    brand: str | None = Field(max_length=255, default=None)
    tag: str | None = Field(max_length=255, default=None)
    keyword: str | None = Field(max_length=255, default=None)


class UserAlert(UserAlertBase, table=True):
    """User category or keyword alert"""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")

    user: "Users" = Relationship(
        back_populates="alerts",
    )


class UserAlertCreate(UserAlertBase):
    user_id: int


class UserAlertResponse(UserAlertBase):
    id: int
    user_id: int


UserAlert.model_rebuild()


# =========================== Query Param Model ===============================
class QueryParams(BaseModel):
    """
    Query params for /alert

    size: user size preference (Senior, Intermediate, Junior, Youth)
    brand: user brand preference
    tag: user tag preference
    kw: keyword, string keyword which to send alerts on
    """

    size: Literal["Senior", "Intermediate", "Junior", "Youth"] | None = Field(
        max_length=255, default=None
    )
    brand: str | None = Field(max_length=255, default=None)
    tag: str | None = Field(max_length=255, default=None)
    kw: str | None = Field(max_length=255, default=None)

    @model_validator(mode="after")
    def at_least_one_required(self) -> "QueryParams":
        if not any([self.size, self.brand, self.tag, self.kw]):
            raise ValueError(
                "At least one of 'size', 'brand', 'tag', or 'kw' must be provided."
            )
        return self
