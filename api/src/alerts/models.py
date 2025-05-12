from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.users.models import Users


# ============================== User Alerts Model ============================
class UserAlertBase(SQLModel):
    size: str | None = Field(max_length=255, default=None)
    brand: str | None = Field(max_length=255, default=None)
    tag: str | None = Field(max_length=255, default=None)
    keyword: str | None = Field(max_length=255, default=None)
    frequency: str = Field(max_length=255, default="daily")


class UserAlert(UserAlertBase, table=True):
    """User category or keyword alert"""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")

    user: "Users" = Relationship(
        back_populates="alerts",
    )


class UserAlertCreate(UserAlertBase):
    pass


class UserAlertResponse(UserAlertBase):
    id: int
    user_id: int


UserAlert.model_rebuild()
