# Define here the models for your scraped items
#
# See documentation in:
# https://docs.org/en/latest/topics/items.html

from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader


class Product(Item):
    url = Field()
    image_urls = Field()
    images = Field()
    title = Field()
    price = Field()
    originalPrice = Field()
    store = Field()


# Helper function to remove dollar symbol from string
def removeDollarSign(s):
    return s[1 : len(s)]


class ProductLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    # default_output_processor = TakeFirst()
    title_out = TakeFirst()
    price_in = MapCompose(removeDollarSign)
    price_out = TakeFirst()
    originalPrice_in = MapCompose(removeDollarSign)
    originalPrice_out = TakeFirst()
