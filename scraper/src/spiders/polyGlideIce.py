from pathlib import Path
from urllib.parse import urljoin

import scrapy

from scraper.src.items import Product, ProductLoader
from scraper.src.utils import read_json


class PolyGlideSpider(scrapy.Spider):
    name = "polyGlideIce"
    website_name = "PolyGlide Ice"
    country = "US"
    base_url = "https://www.polyglidesyntheticice.com/"
    start_urls = [base_url]
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Parse all items from the All Clearance Items page.
        """
        # Holder for manually added values
        manual_vals = {}
        manual_vals["brand"] = "PolyGlide"
        manual_vals["tags"] = ["Synthetic Ice"]

        # Get all products on page
        prods = response.css(self.exp["products"]["css"])

        # Extract product details
        for prod in prods:
            # If not on sale, skip
            if not prod.css(self.exp["product_info"]["original_price"]["css"]).get():
                continue

            # Manually extract sale price
            manual_vals["price"] = prod.css(
                self.exp["product_info"]["price"]["css"]
            ).getall()[-1]

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
