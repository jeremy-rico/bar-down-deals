from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.alerts.models import UserAlert, UserAlertResponse


# ============================== User Models ==================================
class UserBase(SQLModel):
    """User model."""

    email: EmailStr = Field(max_length=255, unique=True, index=True)


class Users(UserBase, table=True):
    """
    User table definition
    NOTE: 'User' is a reserved table name in postgres so we use Users instead
    """

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

    alerts: list["UserAlert"] = Relationship(
        back_populates="user",
        cascade_delete=True,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class UserCreate(UserBase):
    """User creation schema"""

    password: str = Field(min_length=8)


class UserResponse(UserBase):
    """User response schema"""

    id: int
    alerts: list["UserAlertResponse"]


# ============================== JWT Token Model ==============================


class Token(SQLModel):
    """Token schema"""

    access_token: str
    token_type: str = "bearer"


# ============================ Login Data Shema ===============================


class LoginData(SQLModel):
    """Login data schema"""

    email: EmailStr
    password: str
