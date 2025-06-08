from pathlib import Path

import scrapy

from scrapers.stick_scraper.src.items import Price, PriceLoader
from scrapers.stick_scraper.src.utils import read_json

urls = read_json(Path(__file__).parent.parent.parent / "expressions/urls.json")


class PureHockeySpider(scrapy.Spider):

    name = "pureHockey"
    website_name = "Pure Hockey"
    country = "US"
    base_url = "https://www.purehockey.com/"
    start_urls = urls[name].keys()
    exp = read_json(
        Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    )

    def parse(self, response):
        """
        Extract product name, price, currency
        """
        # Get stick id based on url
        stick_id = urls[self.name][response.url]

        # Load item
        l = PriceLoader(item=Price(), selector=response)

        # Add values
        l.add_value("stick_id", stick_id)
        l.add_value("currency", "USD")
        l.add_value("url", response.url)

        # Check for sale price, fall back to original
        if response.css(self.exp["sale_price"]).get():
            l.add_css("price", self.exp["sale_price"])
        else:
            l.add_css("price", self.exp["price"])

        yield l.load_item()
