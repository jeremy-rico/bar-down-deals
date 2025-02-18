from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """User model."""

    email: str = Field(max_length=255, unique=True)


class User(UserBase, table=True):
    """User table definition"""

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    hashed_password: str


class UserCreate(UserBase):
    """User creation schema"""

    password: str


class UserResponse(UserBase):
    """User response schema"""

    id: int


class Token(SQLModel):
    """Token schema"""

    access_token: str
    token_type: str = "bearer"


class LoginData(SQLModel):
    """Login data schema"""

    email: EmailStr
    password: str
