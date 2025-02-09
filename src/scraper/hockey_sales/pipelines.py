# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# import asyncio
# import asyncpg
from datetime import datetime

import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem, NotConfigured


class PostgresPipeline:
    def __init__(self, pg_host, pg_name, pg_user, pg_password, pg_port, pg_table):
        self.pg_host = pg_host
        self.pg_name = pg_name
        self.pg_user = pg_user
        self.pg_password = pg_password
        self.pg_port = pg_port
        self.pg_table = pg_table
        # self.batch_size = batch_size
        # self.loop = loop
        # self.pool = None
        # self.items = []

    @classmethod
    def from_crawler(cls, crawler):
        """
        Grab project settings values
        """
        pg_host = crawler.settings.get("PG_HOST")
        pg_name = crawler.settings.get("PG_NAME")
        pg_user = crawler.settings.get("PG_USER")
        pg_password = crawler.settings.get("PG_PASSWORD")
        pg_port = crawler.settings.get("PG_PORT")
        pg_table = crawler.settings.get("PG_TABLE", "products")
        # batch_size = crawler.settings.getint("PG_BATCH_SIZE", 50)

        if not all([pg_host, pg_name, pg_user, pg_password]):
            raise NotConfigured("PostgreSQL settings are missing")

        # loop = asyncio.get_event_loop()
        return cls(pg_host, pg_name, pg_user, pg_password, pg_port, pg_table)

    def open_spider(self, spider):
        try:
            self.conn = psycopg2.connect(
                host=self.pg_host,
                dbname=self.pg_name,
                user=self.pg_user,
                password=self.pg_password,
                port=self.pg_port,
            )
            self.cur = self.conn.cursor()
            spider.logger.info(f"Successfully connected to {self.pg_name}")
        except Exception as e:
            spider.logger.error(f"Failed to connect to database, {e}")

    def close_spider(self, spider):
        """
        Update website last_scraped and close db connection
        """
        query = f"""
            UPDATE websites 
            SET last_scraped = %s 
            WHERE url = %s;
        """
        values = (datetime.now(), spider.base_url)
        self.cur.execute(query, values)
        self.cur.close()

        self.conn.commit()
        self.conn.close()
        spider.logger.info(f"Closed connection to database {self.pg_name}")

    def validate(self, item):
        adapter = ItemAdapter(item)
        if not adapter.get("price"):
            raise DropItem("Missing Price")

    def process_item(self, item, spider):
        """
        Validate item, insert product and deal to database
        """
        self.validate(item)
        adapter = ItemAdapter(item)
        # columns = ", ".join(adapter.field_names())
        # values = tuple(adapter.values())
        # values_template = ", ".join(["%s" for _ in range(len(values))])
        # query = f"""
        #     INSERT INTO {self.pg_table} ({columns})
        #     VALUES ({values_template});
        #     """
        # values = (
        #     adapter["image_urls"][0],
        #     adapter["images"][0],
        #     adapter["original_price"],
        #     adapter["price"],
        #     adapter["store"],
        #     adapter["title"],
        #     adapter["url"],
        # )
        # self.cur.execute(query, values)
        # self.cur.execute(f"SELECT * FROM {self.pg_table}")
        # data = self.cur.fetchone()
        # print(data)
