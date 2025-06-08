import json
from pathlib import Path

import scrapy

from scrapers.stick_scraper.src.items import Price, PriceLoader
from scrapers.stick_scraper.src.utils import read_json

urls = read_json(Path(__file__).parent.parent.parent / "expressions/urls.json")


class IceWarehouseSpider(scrapy.Spider):
    name = "iceWarehouse"
    website_name = "Ice Warehouse"
    country = "US"
    base_url = "https://www.icewarehouse.com/"
    start_urls = urls[name].keys()
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Extract price
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
        # TODO: Account for prices not stored as ranges
        if response.css(self.exp["sale_price_range"]).get():
            price_range = json.loads(response.css(self.exp["sale_price_range"]).get())
        else:
            price_range = json.loads(response.css(self.exp["price_range"]).get())

        l.add_value("price", str(max(price_range)))

        yield l.load_item()
