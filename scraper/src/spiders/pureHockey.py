from pathlib import Path
from urllib.parse import urlparse

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
        Starting from the clearance page, explore each category link.
        """
        category_links = response.css(self.exp["category_links"]["css"])
        yield from response.follow_all(category_links, self.parse_products)

    def parse_products(self, response):
        """
        Parse all items in category page
        """
        # Get categories from url
        categories = self.get_categories(response.url)

        # Get all products on page
        prods = response.css(self.exp["product_links"]["css"])
        # prods = [prods[0]]  # TODO: Remove this

        # Extract product details
        for prod in prods:
            l = ProductLoader(item=Product(), selector=prod)
            for field_name in l.item.fields.keys():
                if field_name == "categories":
                    l.add_value("categories", categories)
                elif field_name in self.exp["product_info"].keys():
                    l.add_css(field_name, self.exp["product_info"][field_name]["css"])
            yield l.load_item()

        # Follow all next links
        next_links = response.css(self.exp["next_links"]["css"])
        yield from response.follow_all(next_links, self.parse_products)

    def get_categories(self, url: str) -> list[str]:
        """
        Get product categories based on url. More tags are added based on the
        item title in the item pipeline.

        Args:
            url: response url

        Returns:
            list[str]: list of categories
        """
        try:
            url_page = urlparse(url).path.split("/")[-1]
            categories = self.exp["categories"].get(url_page) or []
        except Exception as e:
            print(f"Unable to infer categories from url {url}. Error: {e}")

        return categories
