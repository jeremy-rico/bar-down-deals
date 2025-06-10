import re
from pathlib import Path

import chompjs
import scrapy

from scrapers.stick_scraper.src.items import Price, PriceLoader
from scrapers.stick_scraper.src.utils import get_urls, read_json

# urls = get_urls("bauerHockeyUS")
# urls = read_json(Path(__file__).parent.parent.parent / "expressions/urls.json")

urls = get_urls("bauerHockeyUS")


class BauerHockeyUSSpider(scrapy.Spider):
    """
    Bauer is a bitch and holds all their data behind js. Not able to get any
    category or product links so for this scraper we hardcode each category page
    and extract what we can from a script that has some content.
    """

    name = "bauerHockeyUS"
    website_name = "Bauer Hockey (US)"
    country = "US"
    base_url = "https://www.bauer.com/"
    start_urls = []
    jsonPath = Path(__file__).parent.parent.parent / "expressions" / str(name + ".json")
    exp = read_json(jsonPath)

    def parse(self, response):
        """
        Extract price. Gotta use re to extract sprice from a script in the html.
        This spider will crash if it can't find price.
        """
        # Get stick id based on url
        stick_id = 0
        # stick_id = urls[self.name][response.url]

        # Load item
        l = PriceLoader(item=Price(), selector=response)

        # Add values
        l.add_value("stick_id", stick_id)
        l.add_value("currency", "USD")
        l.add_value("url", response.url)

        # Get prices for all size in this order
        # S, I, J, Y
        price = response.css(self.exp["prices"]).getall()
        price_senior = price[0]
        l.add_value("price", price_senior)

        yield l.load_item()
