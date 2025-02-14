from datetime import datetime

# shared model definitions
from api.src.deals.models import Deal, Product, Website

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from sqlalchemy import URL, select
from sqlalchemy.dialects.postgresql import insert

# database connection
from scraper.src.database import get_session
from scraper.src.utils import get_discount


class PostgresPipeline:
    def __init__(self, database_url: URL):
        self.database_url = database_url

    @classmethod
    def from_crawler(cls, crawler):
        database_url = crawler.settings.get("DATABASE_URL")
        return cls(database_url)

    def open_spider(self, spider):
        """
        Get SQLAlchemy session
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

    def upsert_website(self, spider):
        """
        UPDATE website timestamp or INSERT new website

        Returns:
            Written website
        """
        stmt = (
            insert(Website)
            .values(
                name=spider.website_name,
                url=spider.base_url,
                last_scraped=datetime.now(),
            )
            .on_conflict_do_update(
                index_elements=["url"], set_=dict(last_scraped=datetime.now())
            )
            .returning(Website)
        )

        result = self.session.execute(stmt)
        self.session.commit()

        return result.scalar()

    def upsert_product(self, item):
        """
        INSERT new product or do nothing

        Returns:
            Written or existing product
        """
        stmt = select(Product).where(Product.name == item.get("name"))
        product = self.session.scalars(stmt).first()

        if not product:
            product = Product(
                name=item.get("name"),
                brand=item.get("brand", None),
                category_id=item.get("category_id", None),
                image_url=item.get("images")[0]["path"] if item.get("images") else "",
                description=item.get("description", None),
            )

            self.session.add(product)
            self.session.flush()
            self.session.refresh(product)

        return product

    def process_item(self, item, spider):
        """
        Validate item, upsert website, insert product and deal details to database
        """
        # TODO: Exception handling
        self.validate(item)

        # Insert product details
        product = self.upsert_product(item)

        discount = get_discount(
            item.get("price"),
            item.get("original_price", None),
        )

        # Insert deal details
        deal = Deal(
            product_id=product.id,
            website_id=self.website.id,
            price=item.get("price"),
            original_price=item.get("original_price", None),
            discount=discount,
            url=item.get("url"),
        )
        self.session.add(deal)
        self.session.flush()
