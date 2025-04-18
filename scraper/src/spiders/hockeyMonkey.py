from pathlib import Path
from urllib.parse import urlparse

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
        category_links = category_links[:1]
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
        Extract product details from product list page to minimize number of
        requests made.
        """
        # Get tags based on url
        tags = self.get_tags(response.url)

        # Get all products on page
        prods = response.css(self.exp["product_links"]["css"])
        prods = prods[:1]

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
            return self.exp["tags"].get(url_page)
        except Exception as e:
            print(f"Unable to infer tags from url {url}. Error: {e}")
            return []
