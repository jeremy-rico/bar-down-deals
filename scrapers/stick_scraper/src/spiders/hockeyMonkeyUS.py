from pathlib import Path

import scrapy

from scrapers.site_scraper.src.utils import read_json
from scrapers.stick_scraper.src.items import Price, PriceLoader


class HockeyMonkeyUSStickSpider(scrapy.Spider):

    name = "hockeyMonkeyUS"
    website_name = "Hockey Monkey (US)"
    ships_to = "US"
    base_url = "https://www.hockeymonkey.com/"
    start_urls = [
        base_url + "ccm-hockey-stick-jetspeed-ft7-pro-sr.html",
    ]
    exp = read_json(
        Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    )
    url_map = read_json(
        Path(__file__).parent.parent.parent / "expressions/url_map.json"
    )

    def parse(self, response):
        """
        Extract product name, price, currency
        """
        # Get stick id based on url
        stick_id = self.url_map[response.url]

        # Load item
        l = PriceLoader(item=Price(), selector=response)

        # Add values
        l.add_value("stick_id", stick_id)
        l.add_value("currency", "USD")
        l.add_value("url", response.url)

        # Add css
        for field_name in self.exp.keys():
            l.add_css(field_name, self.exp[field_name])

        yield l.load_item()
