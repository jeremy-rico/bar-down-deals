from pathlib import Path
from urllib.parse import urlparse

import scrapy

from scraper.src.items import Product, ProductLoader
from scraper.src.utils import read_json


class HockeyMonkeyCASpider(scrapy.Spider):
    """
    Hockey Monkey CANADA spider

    NOTE: There are many empty/invisible product instances so this spider will
    raise a lot of 'Dropped: Missing Price' warnings. About three per page. This
    is fine and does not mean the spider is malfunctioning
    """

    name = "hockeyMonkeyCA"
    website_name = "Hockey Monkey (CA)"
    ships_to = "CA"
    base_url = "https://hockeymonkey.ca/"
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
        if category_links:
            yield from response.follow_all(category_links, self.parse)
        else:
            yield from self.parse_products(response)

    def parse_products(self, response):
        """
        Extract product details from product list page to minimize number of
        requests made.
        """
        # Ignore apparel and footwear
        ignore = [
            "clearance-adult-hockey-apparel.html",
            "clearance-youth-hockey-apparel.html",
            "clearance-womens-hockey-apparel.html",
            "clearance-hockey-headwear.html",
        ]
        if response.url.split("/")[-1] in ignore:
            print(f"Ignoring url {response.url}")
            return

        # Get tags based on url
        tags = self.get_tags(response.url)
        print(tags)

        # Get all products on page
        prods = response.css(self.exp["products"]["css"])

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
        tags = []
        try:
            for url_keyword, tag in self.exp["tags"].items():
                if url_keyword in url:
                    tags += tag
        except Exception as e:
            print(f"Unable to infer tags from url {url}. Error: {e}")

        return tags
