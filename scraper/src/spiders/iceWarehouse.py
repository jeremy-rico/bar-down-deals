import json
import re
from pathlib import Path
from urllib.parse import urlparse

import scrapy

from scraper.src.items import Product, ProductLoader
from scraper.src.utils import read_json


class IceWarehouseSpider(scrapy.Spider):
    name = "iceWarehouse"
    website_name = "Ice Warehouse"
    base_url = "https://www.icewarehouse.com/"
    start_urls = [
        base_url + "Clearance_Hockey_Gear/catpage-HOCSALE.html",
    ]
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Starting from the clearance categories page, explore each category link.
        """
        category_links = response.css(self.exp["category_links"]["css"])
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
        # Get categories based on url
        categories = self.get_categories(response.url)

        # Get all products on page
        prods = response.css(self.exp["product_links"]["css"])

        # Price data needs to be scraped manually
        price_range = response.css(self.exp["product_info"]["price_range"]["css"]).get()
        original_price_range = response.css(
            self.exp["product_info"]["original_price_range"]["css"]
        ).get()
        price = response.css(self.exp["product_info"]["price"]["css"]).get()
        original_price = response.css(
            self.exp["product_info"]["original_price"]["css"]
        ).getall()
        if price_range:
            price_data = json.loads(price_range)
            price = str(price_data[len(price_data) // 2])
        if original_price_range:
            print(original_price_range)
            original_price_data = json.loads(original_price_range)
            original_price = str(original_price_data[len(original_price_data) // 2])
        elif original_price:
            original_price = re.findall(r"\d+\.\d+", original_price[0])[1]

        for prod in prods:
            l = ProductLoader(item=Product(), selector=prod)
            for field_name in l.item.fields.keys():
                if field_name == "categories":
                    l.add_value("categories", categories)
                elif field_name == "price":
                    l.add_value("price", price)
                elif field_name == "original_price":
                    l.add_value("original_price", original_price)
                elif field_name in self.exp["product_info"].keys():
                    l.add_css(field_name, self.exp["product_info"][field_name]["css"])
            yield l.load_item()

        # Follow all next links
        # NOTE: Ice Warehouse uses no next links for pagination, but I'm going
        # to leave this in for now. It doesn't do any harm
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
            return categories
        except Exception as e:
            print(f"Unable to infer categories from url {url}. Error: {e}")
            return []
