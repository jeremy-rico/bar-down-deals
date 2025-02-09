import scrapy
from hockey_sales.items import Product, ProductLoader


class HockeyMonkeySpider(scrapy.Spider):
    name = "hockeyMonkey"
    base_url = "https://www.hockeymonkey.com/"  # Used to update db website table
    start_urls = [
        base_url + "clearance.html",
    ]

    def parse(self, response):
        """
        Starting from the clearance categories page, explore each category link.
        """
        category_links = response.css("div.shop-by-category a.sub-category-image")
        category_links = [category_links[0]]  # TODO: REMOVE
        yield from response.follow_all(category_links, self.parse_category)

    def parse_category(self, response):
        """
        Determine if there are subcategories.
        """
        subcategory_links = response.css("div.shop-by-category a")
        if subcategory_links:
            yield from response.follow_all(subcategory_links, self.parse_category)
        else:
            yield from self.parse_products(response)

    def parse_products(self, response):
        """
        Scrape product details, following all next links
        """

        # NOTE: Update css values here
        css_map = {
            "name": "a.product-item-link::text",
            "brand": "strong.brand-name::text",
            # "category": "",
            "url": "a.product-item-link::attr(href)",
            "image_urls": "img.product-image-photo::attr(data-src)",
            "price": "span.normal-price.is-clearance span.price::text",
            "original_price": "span.old-price span.price::text",
        }

        # Get all products on page
        prods = response.css("div.product-item-info")
        prods = [prods[0]]  # TODO: Remove this

        # Extract product details
        for prod in prods:
            l = ProductLoader(item=Product(), selector=prod)
            for field_name, css in css_map.items():
                l.add_css(field_name, css)
            yield l.load_item()

        next_links = response.css("div.pages a.action.next")
        yield from response.follow_all(next_links, self.parse_category)
