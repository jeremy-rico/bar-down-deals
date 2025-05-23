from datetime import datetime, timezone

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.src.database import clean_bucket, clean_database
from scraper.src.spiders.bauerHockeyUS import BauerHockeyUSSpider
from scraper.src.spiders.ccmHockeyCA import CCMHockeyCASpider
from scraper.src.spiders.ccmHockeyUS import CCMHockeyUSSpider
from scraper.src.spiders.discountHockey import DiscountHockeySpider
from scraper.src.spiders.hockeyMonkeyCA import HockeyMonkeyCASpider
from scraper.src.spiders.hockeyMonkeyUS import HockeyMonkeyUSSpider
from scraper.src.spiders.hockeyShot import HockeyShotSpider
from scraper.src.spiders.iceWarehouse import IceWarehouseSpider
from scraper.src.spiders.peranisHockeyWorld import PeranisHockeyWorldSpider
from scraper.src.spiders.polyGlideIce import PolyGlideSpider
from scraper.src.spiders.proHockeyLife import ProHockeyLifeSpider
from scraper.src.spiders.pureGoalie import PureGoalieSpider
from scraper.src.spiders.pureHockey import PureHockeySpider
from scraper.src.utils import get_logger, setup_logging

settings = get_project_settings()

setup_logging()
logger = get_logger(__name__)

logger.info("Beginning crawl...")

spiders = [
    BauerHockeyUSSpider,
    CCMHockeyUSSpider,
    CCMHockeyCASpider,
    DiscountHockeySpider,
    HockeyMonkeyCASpider,
    HockeyMonkeyUSSpider,
    HockeyShotSpider,
    IceWarehouseSpider,
    PeranisHockeyWorldSpider,
    PolyGlideSpider,
    ProHockeyLifeSpider,
    PureGoalieSpider,
    PureHockeySpider,
]
spider_names = [spider.name for spider in spiders]
logger.info(f"Spiders scheduled to crawl: {spider_names}")

start = datetime.now(timezone.utc)
logger.debug(f"Start time: {start} UTC")

# Add all spiders to process
process = CrawlerProcess(settings)
for spider in spiders:
    process.crawl(spider)


# Begin crawl
process.start()

# Get crawl elapsed time
time_elapsed = datetime.now(timezone.utc) - start
logger.debug(f"Crawls completed in {time_elapsed.total_seconds()} seconds")

# Clean database
logger.info(f"Cleaning database...")
clean_database()

# Clean S3
logger.info(f"Cleaning bucket...")
clean_bucket()

# Get total elapsed time
time_elapsed = datetime.now(timezone.utc) - start
logger.info(f"All processes completed in {time_elapsed.total_seconds()} seconds")
