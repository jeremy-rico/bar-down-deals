from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from api.src.aws.utils import clean_bucket
from scraper.src.database import clean_database
from scraper.src.settings import DATABASE_URL
from scraper.src.spiders.discountHockey import DiscountHockeySpider
from scraper.src.spiders.hockeyMonkey import HockeyMonkeySpider
from scraper.src.spiders.iceWarehouse import IceWarehouseSpider
from scraper.src.spiders.peranisHockeyWorld import PeranisHockeyWorldSpider
from scraper.src.spiders.pureHockey import PureHockeySpider

# Crawl all spiders
settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(DiscountHockeySpider)
process.crawl(HockeyMonkeySpider)
process.crawl(PureHockeySpider)
process.crawl(IceWarehouseSpider)
process.crawl(PeranisHockeyWorldSpider)
process.start()

# Delete all deals that haven't been updated in over 48hrs
clean_database(DATABASE_URL)
clean_bucket()
