from itemloaders.processors import MapCompose, TakeFirst
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader

from scrapers.stick_scraper.src.utils import clean_price


class Price(Item):
    stick_id = Field()
    price = Field()
    currency = Field()
    url = Field()


class PriceLoader(ItemLoader):
    # default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    price_in = MapCompose(str.strip, clean_price)
