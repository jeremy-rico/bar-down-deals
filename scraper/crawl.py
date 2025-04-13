import logging
from datetime import datetime, timezone

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.src.database import clean_bucket, clean_database
from scraper.src.settings import DATABASE_URL
from scraper.src.spiders.ccmHockey import CCMHockeySpider
from scraper.src.spiders.discountHockey import DiscountHockeySpider
from scraper.src.spiders.hockeyMonkey import HockeyMonkeySpider
from scraper.src.spiders.iceWarehouse import IceWarehouseSpider
from scraper.src.spiders.peranisHockeyWorld import PeranisHockeyWorldSpider
from scraper.src.spiders.pureHockey import PureHockeySpider

logger = logging.getLogger(__name__)
logging.basicConfig(encoding="utf-8", level=logging.INFO)
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
settings = get_project_settings()
process = CrawlerProcess(settings)
for spider in spiders:
    process.crawl(spider)
# process.start()
time_elapsed = datetime.now(timezone.utc) - start
logging.info(f"Crawl completed in {time_elapsed.total_seconds()} seconds")


# Delete all deals that haven't been updated in over 48hrs
logging.info(f"Cleaning database...")
clean_database(DATABASE_URL)

# Delete all objects in s3 bucket that haven't been updated in 7 days
logging.info(f"Cleaning bucket...")
clean_bucket()

time_elapsed = datetime.now(timezone.utc) - start
logging.info(f"All processes completed in {time_elapsed.total_seconds()} seconds")
