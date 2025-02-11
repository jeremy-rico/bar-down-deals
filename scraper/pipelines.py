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
        Update website timestamp, close db connection
        """
        # self.session.commit()
        self.upsert_website(spider)
        self.session.commit()
        self.session.close()

    def validate(self, item):
        adapter = ItemAdapter(item)
        if not adapter.get("price"):
            raise DropItem("Missing Price")

    def upsert_website(self, spider):
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
        )
        self.session.execute(stmt)
        # return website

    def process_item(self, item, spider):
        self.validate(item)
