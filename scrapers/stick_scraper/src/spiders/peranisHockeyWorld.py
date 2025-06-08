from pathlib import Path

import scrapy

from scrapers.stick_scraper.src.items import Price, PriceLoader
from scrapers.stick_scraper.src.utils import read_json

urls = read_json(Path(__file__).parent.parent.parent / "expressions/urls.json")


class PeranisHockeyWorldSpider(scrapy.Spider):
    name = "peranisHockeyWorld"
    website_name = "Peranis Hockey World"
    country = "US"
    base_url = "https://www.hockeyworld.com/"
    start_urls = urls[name].keys()
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Extract price and size
        """
        # Get stick id based on url
        stick_id = urls[self.name][response.url]

        # Load item
        l = PriceLoader(item=Price(), selector=response)

        # Add values
        l.add_value("stick_id", stick_id)
        l.add_value("currency", "USD")
        l.add_value("url", response.url)

        # Accounts for sale and normal price
        price = response.css(self.exp["price"]).get()
        l.add_value("price", price)

        yield l.load_item()
