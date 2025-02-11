# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Ensure backend folder is in Python path
# from datetime import datetime

import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem, NotConfigured

from api.core.database import get_session


class PostgresPipeline:
    def __init__(self):
        self.session = get_session()

    # @classmethod
    # def from_crawler(cls, crawler):
    #     """
    #     Grab project settings values
    #     """
    #     pass
    #     # pg_host = crawler.settings.get("PG_HOST")
    # pg_name = crawler.settings.get("PG_NAME")
    # pg_user = crawler.settings.get("PG_USER")
    # pg_password = crawler.settings.get("PG_PASSWORD")
    # pg_port = crawler.settings.get("PG_PORT")
    # pg_table = crawler.settings.get("PG_TABLE", "products")
    # # batch_size = crawler.settings.getint("PG_BATCH_SIZE", 50)
    #
    # if not all([pg_host, pg_name, pg_user, pg_password]):
    #     raise NotConfigured("PostgreSQL settings are missing")
    #
    # return cls(pg_host, pg_name, pg_user, pg_password, pg_port, pg_table)

    # def open_spider(self, spider):
    #     try:
    #         self.conn = psycopg2.connect(
    #             host=self.pg_host,
    #             dbname=self.pg_name,
    #             user=self.pg_user,
    #             password=self.pg_password,
    #             port=self.pg_port,
    #         )
    #         self.cur = self.conn.cursor()
    #         spider.logger.info(f"Successfully connected to {self.pg_name}")
    #     except Exception as e:
    #         spider.logger.error(f"Failed to connect to database, {e}")
    #
    # def close_spider(self, spider):
    #     """
    #     Insert or update website db table, close db connection
    #     """
    #     query = f"""
    #         INSERT INTO websites (name, url)
    #         VALUES (%s, %s)
    #         ON CONFLICT (url) DO UPDATE SET last_scraped=NOW();
    #     """
    #     values = (spider.website_name, spider.base_url)
    #     self.cur.execute(query, values)
    #     self.cur.close()
    #
    #     self.conn.commit()
    #     self.conn.close()
    #     spider.logger.info(f"Closed connection to database {self.pg_name}")
    #
    # def validate(self, item):
    #     adapter = ItemAdapter(item)
    #     if not adapter.get("price"):
    #         raise DropItem("Missing Price")
    #
    def process_item(self, item, spider):
        pass

    #     """
    #     Validate item, insert product and deal to database
    #     """
    #     self.validate(item)
    # adapter = ItemAdapter(item)
    # name = item["name"]
    # brand = item["brand"]
    # image_url = item["image_urls"][0]
    # print(name)
    # print(brand)
    # print(image_url)
    # get_prod_id_query = f"""
    #     SELECT id from products JOIN deals
    #     ON name={name}
    # """
    # prod_id = self.cur.execute(query)
    # price = item["price"]
    # original_price = item["original_price"]
    # url = item["url"]
