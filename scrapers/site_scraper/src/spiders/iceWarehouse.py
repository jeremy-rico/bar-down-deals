import json
import re
from pathlib import Path
from urllib.parse import urlparse

import scrapy
from scrapy.selector.unified import Selector

from scrapers.site_scraper.src.items import Product, ProductLoader
from scrapers.site_scraper.src.utils import read_json


class IceWarehouseSpider(scrapy.Spider):
    name = "iceWarehouse"
    website_name = "Ice Warehouse"
    ships_to = "US"
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
        subcategory_links = response.css(self.exp["subcategory_links"]["css"])
        if category_links:
            yield from response.follow_all(category_links, self.parse)
        elif subcategory_links:
            yield from response.follow_all(subcategory_links, self.parse)
        else:
            yield from self.parse_products(response)

    def parse_products(self, response):
        """
        Extract product details from product list page to minimize number of
        requests made.
        """
        # Ignore apparel page
        ignore = [
            "catpage-CSHALFTEAM.html",
            "catpage-SWOMHOAP.html",
        ]
        if response.url.split("/")[-1] in ignore:
            return

        # Get tags based on url
        tags = self.get_tags(response.url)

        # Get all products on page
        prods = response.css(self.exp["product_links"]["css"])

        for prod in prods:
            price, original_price = self.get_pricing(prod)
            image_urls = self.get_image_urls(prod)
            l = ProductLoader(item=Product(), selector=prod)
            for field_name in l.item.fields.keys():
                if field_name == "tags":
                    l.add_value("tags", tags)
                elif field_name == "price":
                    l.add_value("price", price)
                elif field_name == "original_price":
                    l.add_value("original_price", original_price)
                elif field_name == "image_urls":
                    l.add_value("image_urls", image_urls)
                elif field_name == "currency":
                    l.add_value("currency", "USD")
                elif field_name in self.exp["product_info"].keys():
                    l.add_css(field_name, self.exp["product_info"][field_name]["css"])
            yield l.load_item()

        # Follow all next links
        # NOTE: Ice Warehouse uses no next links for pagination, but I'm going
        # to leave this in for now. It doesn't do any harm
        next_links = response.css(self.exp["next_links"]["css"])
        yield from response.follow_all(next_links, self.parse_products)

    def get_pricing(self, product: Selector) -> tuple[str | None, str | None]:
        """
        Extract price data manually. If price is given as a range, take the
        median. Sometimes, sale product div doesn't have the proper .is-sale
        class so we check using a back up selector if the first can't be found

        Args:
            product: a selector of one individual product card

        Returns:
            tuple: (price: str, original_price: str)
        """
        price_range = product.css(self.exp["product_info"]["price_range"]["css"]).get()
        if not price_range:
            # try back up selector
            price_range = product.css(
                self.exp["product_info"]["price_range_bak"]["css"]
            ).get()

        original_price_range = product.css(
            self.exp["product_info"]["original_price_range"]["css"]
        ).get()

        # Sale price given as range
        if price_range:
            price_data = json.loads(price_range)
            price = str(price_data[len(price_data) // 2])
        else:
            price = product.css(self.exp["product_info"]["price"]["css"]).get()
            if not price:
                # Try backup selector
                price = product.css(self.exp["product_info"]["price_bak"]["css"]).get()

        # Original price given as range
        if original_price_range:
            original_price_data = json.loads(original_price_range)
            original_price = str(original_price_data[len(original_price_data) // 2])
        else:
            original_price = product.css(
                self.exp["product_info"]["original_price"]["css"]
            ).getall()
            if original_price:
                # Extract from <script>
                original_price = str(re.findall(r"\d+\.\d+", original_price[0])[1])
            else:
                original_price = None

        return (price, original_price)

    def get_image_urls(self, product: Selector) -> str:
        """
        Manually extract image urls. Some products have multiple image urls, one
        being a blank placeholder. In this case, grab the true image src which
        is the last value in the extracted array.

        Args:
            product: a selector of an individual product

        Returns:
            str: image download url
        """
        image_urls = product.css(
            "img.cattable-wrap-cell-imgwrap-inner-img::attr(src)"
        ).getall()

        if len(image_urls) > 0:
            return image_urls[-1]
        return ""

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
