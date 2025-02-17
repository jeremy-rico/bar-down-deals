from datetime import datetime

# from sqlalchemy import DECIMAL, TIMESTAMP, ForeignKey, String, func
from sqlmodel import Field, Relationship, SQLModel, func


# ======================+====== Website Models ==================================
class WebsiteBase(SQLModel):
    name: str = Field(max_length=255)
    url: str


class Website(WebsiteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    last_scraped: datetime | None = Field(default=func.now())

    deals: list["Deal"] = Relationship(back_populates="website", cascade_delete=True)

    def __repr__(self) -> str:
        return f"Website(id={self.id}, name={self.name}, url={self.url})"


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
    created_at: datetime = Field(default=func.now())

    deals: list["Deal"] = Relationship(back_populates="product", cascade_delete=True)

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name}, brand={self.brand}, created_at={self.created_at}, deals={self.deals})"


# ============================== Deal Models ===================================
class DealBase(SQLModel):

    price: float
    original_price: float | None
    discount: float | None
    url: str


class Deal(DealBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id", ondelete="CASCADE")
    website_id: int = Field(foreign_key="website.id", ondelete="CASCADE")
    scraped_at: datetime = Field(default=func.now())

    product: Product = Relationship(back_populates="deals")
    website: Website = Relationship(back_populates="deals")


class DealPublic(DealBase):
    pass


# class Category(Base):
#     __tablename__ = "categories"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[int] = mapped_column(String(255), unique=True)
#
#     products = relationship("Product", back_populates="category")
