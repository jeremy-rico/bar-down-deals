from pathlib import Path

import scrapy

from scraper.src.items import Product, ProductLoader
from scraper.src.utils import read_json


class HockeyMonkeySpider(scrapy.Spider):
    name = "hockeyMonkey"
    website_name = "Hockey Monkey"
    base_url = "https://www.hockeymonkey.com/"
    start_urls = [
        base_url + "clearance.html",
    ]
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Starting from the clearance categories page, explore each category link.
        """
        category_links = response.css(self.exp["category_links"]["css"])
        category_links = [category_links[0]]  # TODO: REMOVE
        yield from response.follow_all(category_links, self.parse_category)

    def parse_category(self, response):
        """
        Determine if there are subcategories.
        """
        subcategory_links = response.css(self.exp["subcategory_links"]["css"])
        if subcategory_links:
            yield from response.follow_all(subcategory_links, self.parse_category)
        else:
            yield from self.parse_products(response)

    def parse_products(self, response):
        """
        Scrape product details, following all next links
        """
        # Get all products on page
        prods = response.css(self.exp["product_links"]["css"])
        prods = [prods[0]]  # TODO: Remove this

        # Extract product details
        for prod in prods:
            l = ProductLoader(item=Product(), selector=prod)
            for field_name, expression in self.exp["product_info"].items():
                l.add_css(field_name, expression["css"])
            yield l.load_item()

        next_links = response.css(self.exp["next_links"]["css"])
        yield from response.follow_all(next_links, self.parse_category)
