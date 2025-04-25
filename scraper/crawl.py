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
from scraper.src.spiders.hockeyShot import HockeyShotSpider
from scraper.src.spiders.iceWarehouse import IceWarehouseSpider
from scraper.src.spiders.peranisHockeyWorld import PeranisHockeyWorldSpider
from scraper.src.spiders.polyGlideIce import PolyGlideSpider
from scraper.src.spiders.pureGoalie import PureGoalieSpider
from scraper.src.spiders.pureHockey import PureHockeySpider
from scraper.src.utils import get_logger, setup_logging

settings = get_project_settings()

setup_logging()
logger = get_logger(__name__)
configure_logging({"LOG_LEVEL": settings.get("LOG_LEVEL")})

logger.info("Beginning crawl...")

spiders = [
    DiscountHockeySpider,
    HockeyMonkeySpider,
    PureHockeySpider,
    IceWarehouseSpider,
    PeranisHockeyWorldSpider,
    CCMHockeySpider,
    PureGoalieSpider,
    PolyGlideSpider,
    HockeyShotSpider,
]
spider_names = [spider.name for spider in spiders]
logger.info(f"Spiders scheduled to crawl: {spider_names}")

start = datetime.now(timezone.utc)
logger.debug(f"Start time: {start} UTC")

# Crawl all spiders
process = CrawlerProcess(settings)
for spider in spiders:
    process.crawl(spider)
process.start()
time_elapsed = datetime.now(timezone.utc) - start
logger.debug(f"Crawls completed in {time_elapsed.total_seconds()} seconds")


logger.info(f"Cleaning database...")
clean_database(DATABASE_URL)

logger.info(f"Cleaning bucket...")
clean_bucket(DATABASE_URL)

time_elapsed = datetime.now(timezone.utc) - start
logger.info(f"All processes completed in {time_elapsed.total_seconds()} seconds")
