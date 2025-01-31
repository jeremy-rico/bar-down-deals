from pathlib import Path

import scrapy


class HockeySpider(scrapy.Spider):
    # A name used by our spider to be used by the Scrapy cli
    name = "hockey"
    # A list of urls to start scraping at we can continue crawling links from
    # these pages.
    start_urls = [
        "https://quotes.toscrape.com/page/1",
        "https://quotes.toscrape.com/page/2",
    ]

    def parse(self, response):
        """
        A method that will be called to handle the response downloaded from each
        of the requests made in start_urls.

        A Spider typically returns many dictionaries containing the data
        extracted from the page. To do this, we use the yield keyword in the
        callback.
        """
        for quote in response.css("div.quote"):
            yield {
                "author": quote.css("small.author::text").get(),
                "text": quote.css("span.text::text").get(),
                "tags": quote.css("div.tags a.tags::text").getall(),
            }
