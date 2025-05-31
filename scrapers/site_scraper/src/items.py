from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader

from scrapers.site_scraper.src.utils import clean_brand, clean_price


class Product(Item):
    name = Field()
    brand = Field()
    url = Field()
    price = Field()
    original_price = Field()
    image_urls = Field()
    images = Field()
    tags = Field()


class ProductLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    # default_output_processor = TakeFirst()

    brand_in = MapCompose(clean_brand)
    price_in = MapCompose(clean_price)
    original_price_in = MapCompose(clean_price)

    name_out = TakeFirst()
    brand_out = TakeFirst()
    url_out = TakeFirst()
    price_out = TakeFirst()
    original_price_out = TakeFirst()
    store_out = TakeFirst()
