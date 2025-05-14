from typing import TYPE_CHECKING

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.alerts.models import UserAlert, UserAlertResponse


# ============================== User Models ==================================
class UserBase(SQLModel):
    """User model."""

    email: EmailStr = Field(max_length=255, unique=True, index=True)
    country: str = Field(max_length=5, default="US")


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


class UserUpdate(BaseModel):
    """User update schema"""

    email: EmailStr | None = Field(max_length=255, default=None)
    password: str | None = Field(min_length=8, default=None)
    country: str | None = Field(max_length=5, default=None)


class UserResponse(UserBase):
    """User response schema"""

    id: int
    alerts: list["UserAlertResponse"]


# ============================== JWT Token Model ==============================


class Token(SQLModel):
    """Token schema"""

    access_token: str
    token_type: str = "bearer"


# ============================ Login Data Schema ===============================


class LoginData(SQLModel):
    """Login data schema"""

    email: EmailStr
    password: str


# ======================= Password Reset Schemas ==============================
class ForgotPasswordBase(SQLModel):
    """Forgot password schema"""

    email: EmailStr


class ForgotPasswordRequest(ForgotPasswordBase):
    pass


class ForgotPasswordResponse(ForgotPasswordBase):
    token: str


class ResetPasswordRequest(SQLModel):
    """Reset password schema"""

    token: str
    password: str
