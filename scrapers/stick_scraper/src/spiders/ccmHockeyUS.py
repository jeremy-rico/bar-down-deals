from pathlib import Path

import scrapy

from scrapers.stick_scraper.src.items import Price, PriceLoader
from scrapers.stick_scraper.src.utils import read_json

urls = read_json(Path(__file__).parent.parent.parent / "expressions/urls.json")


class CCMHockeyUSSpider(scrapy.Spider):
    name = "ccmHockeyUS"
    website_name = "CCM Hockey (US)"
    country = "US"
    base_url = "https://us.ccmhockey.com/"
    start_urls = urls[name].keys()
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def start_requests(self):
        """
        Enable playwright
        """
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={"playwright": True},
            )

    def parse(self, response):
        """
        Extract price
        """
        # Get stick id based on url
        stick_id = urls[self.name][response.url]

        # Load item
        l = PriceLoader(item=Price(), selector=response)

        # Add values
        l.add_value("stick_id", stick_id)
        l.add_value("currency", "USD")
        l.add_value("url", response.url)

        # Check for sale price, fall back to original
        if response.css(self.exp["sale_price"]).get():
            price = response.css(self.exp["sale_price"]).get()
        else:
            price = response.css(self.exp["price"]).get()

        l.add_value("price", price)
        yield l.load_item()
