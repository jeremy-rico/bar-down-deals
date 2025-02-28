from pathlib import Path

import scrapy

from scraper.src.items import Product, ProductLoader
from scraper.src.utils import read_json


class PureHockeySpider(scrapy.Spider):
    name = "pureHockey"
    website_name = "Pure Hockey"
    base_url = "https://www.purehockey.com/"
    start_urls = [
        base_url + "c/hockey-equipment-sale",
    ]
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Parse all items on sale page
        """
        # Get all products on page
        prods = response.css(self.exp["product_links"]["css"])
        prods = [prods[0]]  # TODO: Remove this

        # Extract product details
        for prod in prods:
            l = ProductLoader(item=Product(), selector=prod)
            for field_name, expression in self.exp["product_info"].items():
                print(f"{field_name}: {response.css(expression['css']).get()}")
                l.add_css(field_name, expression["css"])
            yield l.load_item()

        next_links = response.css(self.exp["next_links"]["css"])
        yield from response.follow_all(next_links, self.parse)
