from pathlib import Path

import scrapy

"""
Find the friendly Scrapy docs and tutorial here: 
https://docs.scrapy.org/en/latest/intro/tutorial.html#intro-tutorial
"""


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

        We can execture the spider using its name from the CLI
        py -m scrapy crawl hockey

        To save the output to a file use:
        py -m scrapy crawl hockey -O hockey.json
        """
        for quote in response.css("div.quote"):
            yield {
                "author": quote.css("small.author::text").get(),
                "text": quote.css("span.text::text").get(),
                "tags": quote.css("div.tags a.tags::text").getall(),
            }
        """
        # Now lets follow the link to the next page
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse) 

        # Or you can use the built in <a> element shortcut
        for a in response.css("li.next a"):
            yield response.follow(a, callback=self.parse)

        # Shorten even further using follow_all (no need for a loop)
        anchors = response.css("li.next a")
        yield from response.follow_all(anchors, callback=self.parse)
        # notice the 'from' keyword
        """

        # Shortening further
        # This will recursivly follow <a> elements nested within <li> elements of class next
        # It auto grabs the href attribute, makes a Request, and calls the parse
        # method on the response.
        yield from response.follow_all(css="li.next a", callback=self.parse)
