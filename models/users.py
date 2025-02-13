from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class User(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str]
