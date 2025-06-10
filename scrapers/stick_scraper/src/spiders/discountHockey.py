from pathlib import Path

import scrapy

from scrapers.stick_scraper.src.items import Price, PriceLoader
from scrapers.stick_scraper.src.utils import get_urls, read_json

urls = get_urls("discountHockey")
# urls = read_json(Path(__file__).parent.parent.parent / "expressions/urls.json")


class DiscountHockeySpider(scrapy.Spider):
    name = "discountHockey"
    website_name = "Discount Hockey"
    country = "US"
    base_url = "https://discounthockey.com/"
    start_urls = list(urls.keys())
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Extract price
        Parse all items from the All Clearance Items page.
        """
        # Get stick id based on url
        stick_id = urls[response.url]

        # Load item
        l = PriceLoader(item=Price(), selector=response)

        # Add values
        l.add_value("stick_id", stick_id)
        l.add_value("currency", "USD")
        l.add_value("url", response.url)

        # This accounts for both regular and sale price
        price = response.css(self.exp["price"]).get()
        l.add_value("price", price)

        yield l.load_item()
