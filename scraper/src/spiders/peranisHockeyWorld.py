from pathlib import Path
from urllib.parse import urljoin, urlparse

import scrapy

from scraper.src.items import Product, ProductLoader
from scraper.src.utils import read_json


class PeranisHockeyWorldSpider(scrapy.Spider):
    name = "peranisHockeyWorld"
    website_name = "Peranis Hockey World"
    base_url = "https://www.hockeyworld.com/"
    start_urls = [
        base_url + "CLEARANCE",
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
        # Get tags based on url
        tags = self.get_tags(response.url)

        # Get all products on page
        prods = response.css(self.exp["product_links"]["css"])

        for prod in prods:
            l = ProductLoader(item=Product(), selector=prod)
            for field_name in l.item.fields.keys():
                if field_name == "tags":
                    l.add_value("tags", tags)
                elif field_name == "url":
                    # Manually create and add url
                    endpoint = prod.css(self.exp["product_info"]["url"]["css"]).get()
                    url = urljoin(self.base_url, endpoint)
                    l.add_value("url", url)
                elif field_name == "image_urls":
                    # Manually create and add image urls
                    endpoint = prod.css(
                        self.exp["product_info"]["image_urls"]["css"]
                    ).get()
                    image_urls = urljoin(self.base_url, endpoint)
                    l.add_value("image_urls", image_urls)
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
