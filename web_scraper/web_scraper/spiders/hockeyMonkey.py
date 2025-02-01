# from pathlib import Path

import scrapy


class PureHockeySpider(scrapy.Spider):
    name = "hockeyMonkey"
    # Start url will be clearance page
    # From here we will navigate to each category on the page
    start_urls = [
        "https://www.hockeymonkey.com/clearance.html",
    ]

    def parse(self, response):
        """
        Follow the href to each category and call the parse_category method
        """
        category_links = response.css("div.shop-by-category a")
        yield from response.follow_all(category_links, self.parse_category)

    def parse_category(self, response):
        """
        Some categories (like hockey sticks) have sub categories
        """
        subcategory_links = response.css("div.shop-by-category a")
        if subcategory_links is not None:
            yield from response.follow_all(subcategory_links, self.parse_category)

        items = response.css("li.item.product.product-item")
        for item in items:
            yield {
                "name": item.css("strong.product.name.product-item-name a::text")
                .get()
                .strip(),
            }
