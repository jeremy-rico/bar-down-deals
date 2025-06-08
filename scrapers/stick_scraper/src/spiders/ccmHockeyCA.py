from pathlib import Path

import scrapy

from scrapers.stick_scraper.src.items import Price, PriceLoader
from scrapers.stick_scraper.src.utils import read_json


class CCMHockeyCASpider(scrapy.Spider):
    name = "ccmHockeyCA"
    website_name = "CCM Hockey (CA)"
    country = "CA"
    base_url = "https://ca.ccmhockey.com/en/"
    start_urls = []
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Parse all items from the All Clearance Items page.
        """
        yield
