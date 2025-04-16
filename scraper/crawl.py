import logging
from datetime import datetime, timezone

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from scraper.src.database import clean_bucket, clean_database
from scraper.src.settings import DATABASE_URL
from scraper.src.spiders.ccmHockey import CCMHockeySpider
from scraper.src.spiders.discountHockey import DiscountHockeySpider
from scraper.src.spiders.hockeyMonkey import HockeyMonkeySpider
from scraper.src.spiders.iceWarehouse import IceWarehouseSpider
from scraper.src.spiders.peranisHockeyWorld import PeranisHockeyWorldSpider
from scraper.src.spiders.pureHockey import PureHockeySpider

settings = get_project_settings()
configure_logging({"LOG_LEVEL": settings.get("LOG_LEVEL")})
logging.info("Beginning crawl...")

spiders = [
    DiscountHockeySpider,
    HockeyMonkeySpider,
    PureHockeySpider,
    IceWarehouseSpider,
    PeranisHockeyWorldSpider,
    CCMHockeySpider,
]
spider_names = [spider.name for spider in spiders]
logging.info(f"Spiders scheduled to crawl: {spider_names}")

start = datetime.now(timezone.utc)
logging.info(f"Start time: {start} UTC")

# Crawl all spiders
process = CrawlerProcess(settings)
for spider in spiders:
    process.crawl(spider)
process.start()
time_elapsed = datetime.now(timezone.utc) - start
logging.info(f"Crawls completed in {time_elapsed.total_seconds()} seconds")


logging.info(f"Cleaning database...")
# DATABASE_URL is not a native scrapy setting so it doesn't appear when using
# get_project_settings()
clean_database(DATABASE_URL)

logging.info(f"Cleaning bucket...")
clean_bucket()

time_elapsed = datetime.now(timezone.utc) - start
logging.info(f"All processes completed in {time_elapsed.total_seconds()} seconds")
