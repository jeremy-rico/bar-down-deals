from pathlib import Path
from urllib.parse import urljoin, urlparse

import scrapy

from scrapers.site_scraper.src.items import Product, ProductLoader
from scrapers.site_scraper.src.utils import read_json


class DiscountHockeySpider(scrapy.Spider):
    name = "discountHockey"
    website_name = "Discount Hockey"
    ships_to = "US"
    base_url = "https://discounthockey.com/"
    start_urls = [
        base_url + "collections/all-clearance-items",
    ]
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Parse all items from the All Clearance Items page.
        """
        # Holder for manually added values
        manual_vals = {}
        manual_vals["currency"] = "USD"

        # Get all products on page
        prods = response.css(self.exp["products"]["css"])

        # Extract product details
        for prod in prods:
            # Manually extract name
            manual_vals["name"] = " ".join(
                prod.css(self.exp["product_info"]["name"]["css"]).getall()
            )

            # Manually extract prices
            prices = prod.css(self.exp["product_info"]["price"]["css"]).getall()
            if len(prices) == 2:
                manual_vals["price"] = prices[0]
                manual_vals["original_price"] = prices[1]

            # Manually extract image_url
            manual_vals["image_urls"] = (
                "https:" + prod.css(self.exp["product_info"]["image_urls"]["css"]).get()
            )

            # Manually extract url
            manual_vals["url"] = urljoin(
                self.base_url, prod.css(self.exp["product_info"]["url"]["css"]).get()
            )

            # Load item
            l = ProductLoader(item=Product(), selector=prod)
            for field_name in l.item.fields.keys():
                if field_name in manual_vals:
                    l.add_value(field_name, manual_vals[field_name])
                elif field_name in self.exp["product_info"]:
                    l.add_css(field_name, self.exp["product_info"][field_name]["css"])

            yield l.load_item()

        # Follow all next links
        next_links = response.css(self.exp["next_links"]["css"])
        yield from response.follow_all(next_links, self.parse)
