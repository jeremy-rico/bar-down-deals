from pathlib import Path

import scrapy

from scrapers.site_scraper.src.items import Product, ProductLoader
from scrapers.site_scraper.src.utils import read_json


class PureGoalieSpider(scrapy.Spider):
    name = "pureGoalie"
    website_name = "Pure Goalie"
    country = "US"
    base_url = "https://goalie.purehockey.com/"
    start_urls = [
        base_url + "c/goalie-equipment-sale",
    ]
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Parse all items from the All Clearance Items page.
        """
        # Get all products on page
        prods = response.css(self.exp["products"]["css"])
        manual_vals = {"currency": "USD"}

        # Extract product details
        for prod in prods:
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
