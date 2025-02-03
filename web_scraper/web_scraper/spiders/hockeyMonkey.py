# from pathlib import Path

import scrapy


class PureHockeySpider(scrapy.Spider):
    name = "hockeyMonkey"
    start_urls = [
        "https://www.hockeymonkey.com/clearance.html",
    ]

    def parse(self, response):
        """
        Follow the href to each category and call the parse_category method
        """
        category_links = response.css("div.shop-by-category a.sub-category-image")
        yield from response.follow_all(category_links, self.parse_category)

    def parse_category(self, response):
        """
        Some categories (like hockey sticks) have sub categories
        """
        items = response.css("div.product-item-info")
        if items:
            items = [items[0]]
            for item in items:
                yield {
                    "url": response.url,
                    "name": item.css("a.product-item-link::text").get().strip(),
                }
        else:
            subcategory_links = response.css("div.shop-by-category a")
            yield from response.follow_all(subcategory_links, self.parse_category)
