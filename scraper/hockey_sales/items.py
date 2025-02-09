from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader

from hockey_sales.utils import removeDollarSign


class Product(Item):
    url = Field()
    image_urls = Field()
    images = Field()
    title = Field()
    price = Field()
    original_price = Field()
    store = Field()


class ProductLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    # default_output_processor = TakeFirst()
    title_out = TakeFirst()
    price_in = MapCompose(removeDollarSign)
    price_out = TakeFirst()
    original_price_in = MapCompose(removeDollarSign)
    original_price_out = TakeFirst()
    store_out = TakeFirst()
    url_out = TakeFirst()
    # image_urls_out = Join()
