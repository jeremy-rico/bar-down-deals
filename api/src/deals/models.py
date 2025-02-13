from datetime import datetime
from typing import Optional

from sqlalchemy import DECIMAL, TIMESTAMP, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.core.database import Base


class Website(Base):
    __tablename__ = "websites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(unique=True)
    last_scraped: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    deals = relationship("Deal", back_populates="website")

    def __repr__(self) -> str:
        return f"Website(id={self.id}, name={self.name}, url={self.url})"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[int] = mapped_column(String(255), unique=True)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # TODO: Find a better way of avoiding duplicate products
    name: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    brand: Mapped[Optional[str]] = mapped_column(String(255))
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL")
    )
    image_url: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    category = relationship("Category", back_populates="products")
    deals = relationship("Deal", back_populates="product")


class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE")
    )
    website_id: Mapped[int] = mapped_column(
        ForeignKey("websites.id", ondelete="CASCADE")
    )
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    original_price: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2))
    discount: Mapped[Optional[float]] = mapped_column(DECIMAL(2, 2))
    url: Mapped[str]
    scraped_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    # Relationships
    product = relationship("Product", back_populates="deals")
    website = relationship("Website", back_populates="deals")
