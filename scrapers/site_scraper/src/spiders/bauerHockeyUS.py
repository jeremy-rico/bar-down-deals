import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import chompjs
import scrapy

from scrapers.site_scraper.src.items import Product, ProductLoader
from scrapers.site_scraper.src.utils import read_json


class BauerHockeyUSSpider(scrapy.Spider):
    """
    Bauer is a bitch and holds all their data behind js. Not able to get any
    category or product links so for this scraper we hardcode each category page
    and extract what we can from a script that has some content.
    """

    name = "bauerHockeyUS"
    website_name = "Bauer Hockey (US)"
    ships_to = "US"
    base_url = "https://www.bauer.com/"
    start_urls = [
        base_url + "collections/hockey-sticks-on-sale",
        base_url + "collections/hockey-skates-on-sale",
        base_url + "collections/protective-equipment-on-sale",
        # base_url + "collections/athletic-apparel-on-sale",
    ]
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Parse all items from each starting page.
        """
        # Holder for manually added values
        tags = self.get_tags(response.url)

        # Get all products on page
        script = response.xpath(self.exp["script"]["xpath"]).get()
        match = re.search(r"items:\s*(\[[^\]]+\])", script)

        if match:
            prods_js = match.group(1)
            prods = chompjs.parse_js_object(prods_js)
            for prod in prods:
                url = urljoin(self.base_url,f"products/{prod["handle"]}")
                image_urls = "https:"+prod["image"]
                l = ProductLoader(item=Product(), selector=prod)
                l.add_value("name", prod["name"].title())
                l.add_value("brand", prod["brand"])
                l.add_value("url", url)
                l.add_value("tags", tags)
                l.add_value("price", prod["price"])
                l.add_value("image_urls", image_urls)
                l.add_value("original_price", prod["compareAtPrice"])

                yield l.load_item()

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
            return self.exp["tags"].get(url_page)
        except Exception as e:
            print(f"Unable to infer tags from url {url}. Error: {e}")
            raise
