from sqlalchemy import (
    DECIMAL,
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from api.core.database import Base


class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    url = Column(Text, nullable=False, unique=True)
    last_scraped = Column(TIMESTAMP, default=None)

    deals = relationship("Deal", back_populates="website")

    def __repr__(self) -> str:
        return f"Website(id={self.id}, name={self.name}, url={self.url})"


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    image_url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    category = relationship("Category", back_populates="products")
    deals = relationship("Deal", back_populates="product")


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    website_id = Column(
        Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False
    )
    price = Column(DECIMAL(10, 2), nullable=False)
    original_price = Column(DECIMAL(10, 2), nullable=True)
    url = Column(Text, nullable=False)
    scraped_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    product = relationship("Product", back_populates="deals")
    website = relationship("Website", back_populates="deals")
