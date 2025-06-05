from datetime import datetime, timezone

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapers.stick_scraper.src.logging import get_logger, setup_logging
from scrapers.stick_scraper.src.spiders.hockeyMonkeyUS import HockeyMonkeyUSStickSpider
from scrapers.stick_scraper.src.spiders.pureHockey import PureHockeyStickSpider
from scrapers.stick_scraper.src.utils import fetch_usd_exchange_rates, update_sticks

settings = get_project_settings()

setup_logging()
logger = get_logger(__name__)

logger.info("Beginning stick crawl...")

spiders = [
    HockeyMonkeyUSStickSpider,
    PureHockeyStickSpider,
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

logger.info("Updating sticks...")
update_sticks()

logger.info("Updating exchange rates...")
fetch_usd_exchange_rates()

time_elapsed = datetime.now(timezone.utc) - start
logger.info(f"All processes completed in {time_elapsed.total_seconds()} seconds")
