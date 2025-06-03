from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

# shared model definitions
from api.src.deals.models import Website
from api.src.sticks.models import Stick, StickPrice

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from sqlalchemy import URL, select
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import col

# database connection
from scrapers.site_scraper.src.database import get_session
from scrapers.site_scraper.src.utils import get_discount, get_logger, read_json

logger = get_logger(__name__)


class PostgresPipeline:
    def __init__(self, database_url: URL, s3_host: str):
        self.database_url = database_url
        self.s3_host = s3_host

    @classmethod
    def from_crawler(cls, crawler):
        database_url = crawler.settings.get("DATABASE_URL")
        s3_host = crawler.settings.get("S3_HOST")
        return cls(database_url, s3_host)

    def open_spider(self, spider):
        """
        Get db session
        """
        self.session = get_session()
        stmt = select(Website).where(Website.name == spider.website_name)
        self.website = self.session.scalar(stmt)

    def close_spider(self, spider):
        """
        Close db connection
        """
        try:
            self.session.commit()
        except Exception as e:
            print(f"Failed to close spider: {e}")
            self.session.rollback()
        self.session.close()

    def validate(self, item):
        adapter = ItemAdapter(item)
        # Missing price
        if not adapter.get("price"):
            raise DropItem("Missing Price")

    def update_stick(self, item) -> Stick:
        """
        Update stick if necessary
        """
        stmt = select(Stick).where(Stick.id == item.get("stick_id"))
        result = self.session.execute(stmt)
        stick = result.scalar_one()
        stick.updated_at = datetime.now(timezone.utc)

        if item.get("price") < stick.price:
            stick.price = item.get("price")
            stick.currency = item.get("currency")
            self.session.add(stick)
            try:
                self.session.commit()
                self.session.refresh(stick)
            except Exception as e:
                logger.warning(f"Failed to insert price: {e}")
                self.session.rollback()
        return stick

    def insert_price(self, item) -> StickPrice:
        """
        INSERT new price

        Returns:
           Product
        """
        # Create price object
        price = StickPrice(
            stick_id=item.get("stick_id"),
            website_id=self.website.id,
            price=item.get("price"),
            currency=item.get("currency"),
            url=item.get("url"),
            timestamp=datetime.now(timezone.utc),
        )
        self.session.add(price)
        try:
            self.session.commit()
            self.session.refresh(price)
        except Exception as e:
            logger.warning(f"Failed to insert price: {e}")
            self.session.rollback()

        return price

    def process_item(self, item, spider) -> StickPrice:
        """
        Validate item, insert price
        """
        self.validate(item)

        # Insert price
        price = self.insert_price(item)

        return price


class CustomImagePipeline(ImagesPipeline):
    """
    Defines custom headers for images downloads. Bypasses cloudflare image
    blocking
    """

    def get_media_requests(self, item, info):
        referer = item.get("url")
        for image_url in item.get("image_urls", []):
            yield Request(
                image_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                    "Referer": referer,  # Replace with actual page URL hosting the image
                },
            )


def get_extra_tags(title: str, start_tags: list[str] | None) -> list[str]:
    """
    Helper function to get extra tags in product title that can't be inferred from url

    Args:
      title: Product title
      start_tags: Product tags pulled from url

    Returns:
      List[str]: list of all tags
    """
    all_tags = set(start_tags) if start_tags else set()

    # Get keyword --> tag map
    json_path = Path(__file__).parent.parent / "expressions" / "tags.json"
    keywords = read_json(json_path)
    title = title.lower()

    for kw in keywords.keys():
        if kw in title:
            all_tags.update(keywords[kw])

    return list(all_tags)


def get_brand(name: str, scraped_brand: str | None) -> str | None:
    """
    Helper function to get brand from title if it can't be scraped, OR combine
    brand variations into one.

    Args:
      name: Product name
      brand: scraped product brand
      start_tags: Product tags pulled from url

    Returns:
      str | None: brand OR None
    """
    # Get keyword --> tag map
    json_path = Path(__file__).parent.parent / "expressions" / "brands.json"
    brands_map = read_json(json_path)

    # If we scraped a brand, normalize its name and return
    # Ex: CCM Jetspeed, CCM QuickLite, CCM Ribcore all get turned to CCM
    if scraped_brand:
        for brand, brand_name in brands_map.items():
            if brand in scraped_brand.lower():
                return brand_name

    # Otherwise try to scrape brand from title
    for brand, brand_name in brands_map.items():
        if brand in name.lower():
            return brand_name

    # If we still can't find a brand, return None
    return None
