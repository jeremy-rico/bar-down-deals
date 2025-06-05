from pathlib import Path
from urllib.parse import urljoin, urlparse

import scrapy

from scrapers.site_scraper.src.items import Product, ProductLoader
from scrapers.site_scraper.src.utils import read_json


class CCMHockeyCASpider(scrapy.Spider):
    name = "ccmHockeyCA"
    website_name = "CCM Hockey (CA)"
    country = "CA"
    base_url = "https://ca.ccmhockey.com/en/"
    start_urls = [
        base_url + "Sale/Skates",
        base_url + "Sale/Sticks",
        base_url + "Sale/Protective/Gloves",
        base_url + "Sale/Protective/Pants",
        base_url + "Sale/Protective/Shoulder-Pads",
        base_url + "Sale/Protective/Elbow-Pads",
        base_url + "Sale/Protective/Shin-Guards",
        base_url + "Sale/Goalie",
        base_url + "Sale/Accessories",
    ]
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Parse all items from the All Clearance Items page.
        """
        # Holder for manually added values
        manual_vals = {}
        manual_vals["brand"] = "CCM"
        manual_vals["tags"] = self.get_tags(response.url)
        manual_vals["currency"] = "USD"

        # Get all products on page
        prods = response.css(self.exp["products"]["css"])

        # Extract product details
        for prod in prods:
            # Manually extract original price
            original_price = prod.css(
                self.exp["product_info"]["original_price"]["css"]
            ).getall()
            manual_vals["original_price"] = "".join(original_price)

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
        # NOTE: CCM doesn't use next links, but keeping this doesnt hurt in case
        # they change one day
        next_links = response.css(self.exp["next_links"]["css"])
        yield from response.follow_all(next_links, self.parse)

    def get_tags(self, url: str) -> list[str]:
        """
        Get tags based on url
        """
        url_end = url.split("/")[-1]
        return self.exp["tags"][url_end]
