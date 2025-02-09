from hockey_sales.utils import cleanBrand, cleanPrice
from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader


class Product(Item):
    name = Field()
    brand = Field()
    category = Field()
    description = Field()
    url = Field()
    image_urls = Field()
    images = Field()
    price = Field()
    original_price = Field()
    website = Field()


class ProductLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    # default_output_processor = TakeFirst()
    brand_in = MapCompose(cleanBrand)
    price_in = MapCompose(cleanPrice)
    original_price_in = MapCompose(cleanPrice)

    name_out = TakeFirst()
    brand_out = TakeFirst()
    category_out = TakeFirst()
    description_out = TakeFirst()
    url_out = TakeFirst()
    price_out = TakeFirst()
    original_price_out = TakeFirst()
    store_out = TakeFirst()
