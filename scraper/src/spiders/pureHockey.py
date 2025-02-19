import json
from pathlib import Path

import scrapy

from scraper.src.items import Product, ProductLoader
from scraper.src.settings import SCRAPERAPI_KEY
from scraper.src.utils import get_proxy_url, read_json


class HockeyMonkeySpider(scrapy.Spider):
    name = "pureHockey"
    website_name = "Pure Hockey"
    base_url = "https://www.purehockey.com/"
    start_urls = [
        get_proxy_url(SCRAPERAPI_KEY, base_url + "c/hockey-equipment-sale"),
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

        # Follow next page links
        next_page = response.css(self.exp["next_links"]["css"]).get()
        if next_page is not None:
            next_page = self.base_url + next_page
            print(next_page)
            yield response.follow(get_proxy_url(SCRAPERAPI_KEY, next_page), self.parse)

        # next_links = response.css(self.exp["next_links"]["css"])
        # yield from response.follow_all(next_links, self.parse)

    # def parse(self, response):
    #     """
    #     Starting from the clearance categories page, explore each category link.
    #     """
    #     category_links = response.css(self.exp["category_links"]["css"])
    #     category_links = [category_links[0]]  # TODO: REMOVE
    #     yield from response.follow_all(category_links, self.parse_category)
    #
    # def parse_category(self, response):
    #     """
    #     Determine if there are subcategories.
    #     """
    #     subcategory_links = response.css(self.exp["subcategory_links"]["css"])
    #     if subcategory_links:
    #         yield from response.follow_all(subcategory_links, self.parse_category)
    #     else:
    #         yield from self.parse_products(response)
    #
    # def parse_products(self, response):
    #     """
    #     Scrape product details, following all next links
    #     """
    #
    #     # Get all products on page
    #     prods = response.css(self.exp["product_links"]["css"])
    #     prods = [prods[0]]  # TODO: Remove this
    #
    #     # Extract product details
    #     for prod in prods:
    #         l = ProductLoader(item=Product(), selector=prod)
    #         for field_name, expression in self.exp["product_info"].items():
    #             l.add_css(field_name, expression["css"])
    #         yield l.load_item()
    #
    #     next_links = response.css(self.exp["next_links"]["css"])
    #     yield from response.follow_all(next_links, self.parse_category)
