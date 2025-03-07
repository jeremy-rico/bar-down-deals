import logging
from datetime import datetime, timezone
from urllib.parse import urljoin

# shared model definitions
from api.src.deals.models import Deal, Website
from api.src.products.models import Category, Product

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from sqlalchemy import URL, select
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import col

# database connection
from scraper.src.database import get_session
from scraper.src.utils import get_discount


class PostgresPipeline:
    def __init__(self, database_url: URL, s3_host: str):
        self.database_url = database_url
        self.s3_host = s3_host

    @classmethod
    def from_crawler(cls, crawler):
        database_url = crawler.settings.get("DATABASE_URL")
        logging.getLogger("botocore").setLevel(crawler.settings.get("BOTO_LOG_LEVEL"))
        s3_host = crawler.settings.get("S3_HOST")
        return cls(database_url, s3_host)

    def open_spider(self, spider):
        """
        Get db session
        """
        self.session = get_session(self.database_url)
        self.website = self.upsert_website(spider)

    def close_spider(self, spider):
        """
        Close db connection
        """
        self.session.commit()
        self.session.close()

    def validate(self, item):
        adapter = ItemAdapter(item)
        if not adapter.get("price"):
            raise DropItem("Missing Price")

    def upsert_website(self, spider) -> Website:
        """
        UPDATE website timestamp or INSERT new website

        Returns:
            Website
        """
        stmt = (
            insert(Website)
            .values(
                name=spider.website_name,
                url=spider.base_url,
                updated_at=datetime.now(timezone.utc),
            )
            .on_conflict_do_update(
                index_elements=["url"], set_=dict(updated_at=datetime.now(timezone.utc))
            )
            .returning(Website)
        )

        website = self.session.execute(stmt)
        self.session.commit()

        return website.scalars().one()

    def upsert_product(self, item) -> Product:
        """
        INSERT new product or do nothing

        Returns:
           Product
        """

        stmt = select(Category).where(col(Category.name).in_(item.get("categories")))
        categories = list(self.session.scalars(stmt).all())

        stmt = select(Product).where(Product.name == item.get("name"))
        product = self.session.scalar(stmt)
        if product:
            return product

        image_url = item.get("images")[0]
        if image_url:
            image_url = urljoin(self.s3_host, image_url.get("path"))

        product = Product(
            name=item.get("name"),
            brand=item.get("brand", None),
            categories=categories,
            image_url=image_url if image_url else self.s3_host,
            description=item.get("description", None),
            created_at=datetime.now(timezone.utc),
        )
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)

        return product

    def upsert_deal(self, item, product) -> Deal:
        """
        INSERT deal or UPDATE price and updated_at

        Returns:
            Deal
        """
        discount = get_discount(
            item.get("price"),
            item.get("original_price", None),
        )

        stmt = (
            insert(Deal)
            .values(
                product_id=product.id,
                website_id=self.website.id,
                price=item.get("price"),
                original_price=item.get("original_price", None),
                discount=discount,
                url=item.get("url"),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            .on_conflict_do_update(
                index_elements=["url"],
                set_=dict(
                    price=item.get("price"), updated_at=datetime.now(timezone.utc)
                ),
            )
            .returning(Deal)
        )

        deal = self.session.execute(stmt)
        self.session.commit()

        return deal.scalars().one()

    def process_item(self, item, spider) -> Deal:
        """
        Validate item, upsert product and deal info to database
        """
        # TODO: Exception handling
        self.validate(item)

        # Insert product details
        product = self.upsert_product(item)

        # Insert deal details
        deal = self.upsert_deal(item, product)
        return deal
