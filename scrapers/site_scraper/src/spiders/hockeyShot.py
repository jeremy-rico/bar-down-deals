import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import chompjs
import scrapy

from scrapers.site_scraper.src.items import Product, ProductLoader
from scrapers.site_scraper.src.utils import read_json


class HockeyShotSpider(scrapy.Spider):
    """
    Scrape available data from a script. No original_price available. If you
    happen to see a hockeyShot deal on the site, manually enter the original
    price :)
    """

    name = "hockeyShot"
    website_name = "Hockey Shot"
    ships_to = "US"
    base_url = "https://hockeyshot.com/"
    start_urls = [base_url + "collections/dryland-accessories-sale"]
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Parse all items from each starting page.
        """
        # Holder for manually added values
        brand = "Hockey Shot"
        tags = ["Training"]

        # Get all products on page
        script = response.css(self.exp["script"]["css"]).get()
        match = re.search(r'"productVariants":\s*(\[[^\]]+\])', script)

        if match:
            prods_js = match.group(1)
            prods = chompjs.parse_js_object(prods_js)
            for prod in prods:
                url = urljoin(response.url, prod["product"]["url"])
                image_urls = "https:" + prod["image"]["src"]
                l = ProductLoader(item=Product(), selector=prod)
                l.add_value("name", prod["product"]["title"].title())
                l.add_value("brand", brand)
                l.add_value("url", url)
                l.add_value("tags", tags)
                l.add_value("price", str(prod["price"]["amount"]))
                l.add_value("currency", "USD")
                l.add_value("image_urls", image_urls)

                yield l.load_item()
