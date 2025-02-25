from datetime import datetime
from decimal import Decimal

# from sqlalchemy import DECIMAL, TIMESTAMP, ForeignKey, String, func
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, UniqueConstraint


# ======================+====== Website Models ==================================
class WebsiteBase(SQLModel):
    name: str = Field(max_length=255)
    url: str = Field(unique=True)


class Website(WebsiteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    last_scraped: datetime = Field(sa_column=Column(DateTime(timezone=True)))

    deals: list["Deal"] = Relationship(back_populates="website", cascade_delete=True)

    def __repr__(self) -> str:
        return f"Website(id={self.id}, name={self.name}, url={self.url})"


class WebsiteResponse(WebsiteBase):
    id: int


# ============================= Product Models =================================
class ProductBase(SQLModel):
    # TODO: Find a better way of avoiding duplicate products
    name: str = Field(max_length=255, index=True, unique=True)
    brand: str | None = Field(max_length=255)
    image_url: str | None
    description: str | None


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # category_id: int | None = Field(default=None, foreign_key="category.id")
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))

    deals: list["Deal"] = Relationship(back_populates="product", cascade_delete=True)

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name}, brand={self.brand}, created_at={self.created_at}, deals={self.deals})"


class ProductResponse(ProductBase):
    id: int


# ============================== Deal Models ===================================
class DealBase(SQLModel):
    price: Decimal = Field(max_digits=10, decimal_places=2)
    original_price: Decimal | None = Field(max_digits=10, decimal_places=2)
    discount: Decimal | None = Field(max_digits=4, decimal_places=2)
    url: str


class Deal(DealBase, table=True):
    __table_args__ = (UniqueConstraint("price", "url", name="price_url_unique"),)

    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", ondelete="CASCADE")
    website_id: int = Field(foreign_key="website.id", ondelete="CASCADE")
    last_scraped: datetime = Field(sa_column=Column(DateTime(timezone=True)))

    product: Product = Relationship(
        back_populates="deals", sa_relationship_kwargs={"lazy": "selectin"}
    )
    website: Website = Relationship(
        back_populates="deals", sa_relationship_kwargs={"lazy": "selectin"}
    )


class DealCreate(DealBase):
    pass


class DealResponse(DealBase):
    id: int
    # product_id: int
    # website_id: int
    last_scraped: datetime
    product: ProductResponse
    website: WebsiteResponse


# class Category(Base):
#     __tablename__ = "categories"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[int] = mapped_column(String(255), unique=True)
#
#     products = relationship("Product", back_populates="category")
