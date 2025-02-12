from datetime import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from sqlalchemy import URL, select
from sqlalchemy.dialects.postgresql import insert

# shared model definitions
from api.src.products.models import Category, Deal, Product, Website

# database connection
from scraper.database import get_session


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

    def close_spider(self, spider):
        """
        Close db connection
        """
        self.session.close()

    def validate(self, item):
        adapter = ItemAdapter(item)
        if not adapter.get("price"):
            raise DropItem("Missing Price")

    def upsert_website(self, spider):
        """
        INSERT new website or UPDATE existing website's last_scraped timestamp

        Returns:
            Written website object
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

    def process_item(self, item, spider):
        """
        Validate item, upsert website, insert product and deal details to database
        """
        # TODO: Exception handling
        self.validate(item)

        # Upsert website
        website = self.upsert_website(spider)

        # Insert product details
        product = Product(
            name=item["name"],
            brand=item["brand"],
            # category_id
            image_url=item["images"][0]["path"],
            # description=
        )
        self.session.add(product)
        self.session.flush()

        # Insert deal details
        deal = Deal(
            product_id=product.id,
            website_id=website.id,
            price=item["price"],
            original_price=item["original_price"],
            url=item["url"],
        )
        self.session.add(deal)
        self.session.flush()
