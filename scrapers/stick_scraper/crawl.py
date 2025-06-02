from datetime import datetime, timezone

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapers.site_scraper.src.spiders.bauerHockeyUS import BauerHockeyUSSpider
from scrapers.site_scraper.src.spiders.ccmHockeyCA import CCMHockeyCASpider
from scrapers.site_scraper.src.spiders.ccmHockeyUS import CCMHockeyUSSpider
from scrapers.site_scraper.src.spiders.discountHockey import DiscountHockeySpider
from scrapers.site_scraper.src.spiders.hockeyMonkeyCA import HockeyMonkeyCASpider
from scrapers.site_scraper.src.spiders.hockeyShot import HockeyShotSpider
from scrapers.site_scraper.src.spiders.iceWarehouse import IceWarehouseSpider
from scrapers.site_scraper.src.spiders.peranisHockeyWorld import (
    PeranisHockeyWorldSpider,
)
from scrapers.site_scraper.src.spiders.polyGlideIce import PolyGlideSpider
from scrapers.site_scraper.src.spiders.proHockeyLife import ProHockeyLifeSpider
from scrapers.site_scraper.src.spiders.pureGoalie import PureGoalieSpider
from scrapers.site_scraper.src.spiders.pureHockey import PureHockeyStickSpider
from scrapers.site_scraper.src.utils import get_logger, setup_logging
from scrapers.stick_scraper.src.spiders.hockeyMonkeyUS import HockeyMonkeyUSStickSpider

settings = get_project_settings()

setup_logging()
logger = get_logger(__name__)

logger.info("Beginning stick crawl...")

spiders = [
    # BauerHockeyUSSpider,
    # CCMHockeyUSSpider,
    # CCMHockeyCASpider,
    # DiscountHockeySpider,
    # HockeyMonkeyCASpider,
    HockeyMonkeyUSStickSpider,
    # HockeyShotSpider,
    # IceWarehouseSpider,
    # PeranisHockeyWorldSpider,
    # PolyGlideSpider,
    # ProHockeyLifeSpider,
    # PureGoalieSpider,
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

# Get total elapsed time
time_elapsed = datetime.now(timezone.utc) - start
logger.info(f"Completed in {time_elapsed.total_seconds()} seconds")
