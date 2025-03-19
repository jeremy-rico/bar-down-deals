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
        # category_links = [category_links[0]]  # TODO: REMOVE
        yield from response.follow_all(category_links, self.parse_category)

    def parse_category(self, response):
        """
        Determine if there are subcategories.
        """
        subcategory_links = response.css(self.exp["subcategory_links"]["css"])
        if subcategory_links:
            yield from response.follow_all(subcategory_links, self.parse_category)
        else:
            yield from self.parse_products_page(response)

    def parse_products_page(self, response):
        """
        Follow all product links to go to individual product page, follow all
        next page links
        """
        # Get categories based on url
        categories = self.get_categories(response.url)

        # Get all products on page
        prods = response.css(self.exp["product_links"]["css"])
        # prods = [prods[0]]  # TODO: REMOVE
        cb_kwargs = dict(
            args={
                "brand": response.css(self.exp["product_info"]["brand"]["css"]).get(),
                "image_urls": response.css(
                    self.exp["product_info"]["image_urls"]["css"]
                ).get(),
                "categories": categories,
            }
        )
        yield from response.follow_all(prods, self.parse_product, cb_kwargs=cb_kwargs)

        # Follow all next links
        next_links = response.css(self.exp["next_links"]["css"])
        yield from response.follow_all(next_links, self.parse_products_page)

    def parse_product(self, response, args):
        """
        Scrape product details, following all next links
        """
        l = ProductLoader(item=Product(), selector=response)
        for field_name in l.item.fields.keys():
            if field_name in args:
                l.add_value(field_name, args[field_name])
            elif field_name in self.exp["product_info"].keys():
                l.add_css(field_name, self.exp["product_info"][field_name]["css"])
            elif field_name == "url":
                l.add_value("url", response.url)
        yield l.load_item()

    def get_categories(self, url: str) -> list[str]:
        """
        Get product categories based on url

        Args:
            url: response url

        Returns:
            list[str]: list of categories
        """
        url_path = urlparse(url).path.split("/")
        categories = []
        try:
            for p in url_path[2:]:
                categories += self.exp["categories"][p]
        except Exception as e:
            print(f"Unable to infer categories from url {url}. Error: {e}")

        return categories
