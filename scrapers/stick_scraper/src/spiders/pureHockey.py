from pathlib import Path
from urllib.parse import urlparse

import scrapy

from scrapers.site_scraper.src.items import Product, ProductLoader
from scrapers.site_scraper.src.utils import read_json


class PureHockeySpider(scrapy.Spider):
    name = "pureHockey"
    website_name = "Pure Hockey"
    ships_to = "US"
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
        # NOTE: Skip apparel, its too much clutter
        if response.url.endswith("hockey-apparel-sale"):
            return

        # Get tags from url
        tags = self.get_tags(response.url)

        # Get all products on page
        prods = response.css(self.exp["product_links"]["css"])

        # Extract product details
        for prod in prods:
            l = ProductLoader(item=Product(), selector=prod)
            for field_name in l.item.fields.keys():
                if field_name == "tags":
                    l.add_value("tags", tags)
                elif field_name in self.exp["product_info"].keys():
                    l.add_css(field_name, self.exp["product_info"][field_name]["css"])
            yield l.load_item()

        # Follow all next links
        next_links = response.css(self.exp["next_links"]["css"])
        yield from response.follow_all(next_links, self.parse_products)

    def get_tags(self, url: str) -> list[str]:
        """
        Get product tags based on url. More tags are added based on the
        item title in the item pipeline.

        Args:
            url: response url

        Returns:
            list[str]: list of tags
        """
        try:
            url_page = urlparse(url).path.split("/")[-1]
            tags = self.exp["tags"].get(url_page) or []
            return tags
        except Exception as e:
            print(f"Unable to infer tags from url {url}. Error: {e}")
            return []
