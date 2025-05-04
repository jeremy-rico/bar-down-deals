from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

# shared model definitions
from api.src.deals.models import Deal, Website
from api.src.products.models import Product, Tag
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from sqlalchemy import URL, select
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import col

# database connection
from scraper.src.database import get_session
from scraper.src.utils import get_discount, get_logger, read_json

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
        self.website = self.upsert_website(spider)

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
        # Missing final price
        if not adapter.get("price"):
            raise DropItem("Missing Price")

        # Sale price not less than original price (No sale)
        if adapter.get("price") and adapter.get("original_price"):
            if float(adapter["price"]) >= float(adapter["original_price"]):
                raise DropItem("No Sale")

    def upsert_website(self, spider) -> Website:
        """
        UPDATE website timestamp or INSERT new website

        Returns:
            Website
        """
        stmt = (
            insert(Website)
            .values(
                name=spider.website_name,
                url=spider.base_url,
                updated_at=datetime.now(timezone.utc),
            )
            .on_conflict_do_update(
                index_elements=["url"], set_=dict(updated_at=datetime.now(timezone.utc))
            )
            .returning(Website)
        )

        website = self.session.execute(stmt)
        try:
            self.session.commit()
        except Exception as e:
            logger.warning(f"Failed to upsert website: {e}")
            self.session.rollback()

        return website.scalars().one()

    def upsert_product(self, item) -> Product:
        """
        INSERT new product or UPDATE if needed

        Returns:
           Product
        """

        # Create image url
        image_url = item.get("images")
        if image_url:
            image_url = urljoin(self.s3_host, image_url[0].get("path"))
        else:
            image_url = self.s3_host

        # Create tags
        tags_list = get_extra_tags(item.get("name"), item.get("tags"))
        stmt = select(Tag).where(col(Tag.name).in_(tags_list))
        tags = list(self.session.scalars(stmt).all())

        # Check if products exist
        stmt = select(Product).where(Product.name == item.get("name"))
        product = self.session.scalar(stmt)

        # Update some product info if necessary and return
        if product:
            update = False
            if product.tags != tags:
                update = True
                product.tags = tags
            if product.image_url != image_url:
                update = True
                product.image_url = image_url
            if update:
                try:
                    self.session.add(product)
                    self.session.commit()
                    self.session.refresh(product)
                    logger.info(f"Updated product id {product.id}")
                except Exception as e:
                    logger.warning(f"Failed to update product: {e}")
                    self.session.rollback()
            return product

        # Get brand if it wasn't scraped
        if item.get("brand") == None:
            item["brand"] = get_brand(item.get("name"))

        # Create Product instance and write to db
        product = Product(
            name=item.get("name"),
            brand=item.get("brand", None),
            tags=tags,
            image_url=image_url,
            created_at=datetime.now(timezone.utc),
        )
        self.session.add(product)
        try:
            self.session.commit()
            self.session.refresh(product)
        except Exception as e:
            logger.warning(f"Failed to insert product: {e}")
            self.session.rollback()

        return product

    def upsert_deal(self, item, product) -> Deal:
        """
        INSERT deal or UPDATE price and updated_at

        Returns:
            Deal
        """
        discount = get_discount(
            item.get("price"),
            item.get("original_price", None),
        )

        stmt = (
            insert(Deal)
            .values(
                product_id=product.id,
                website_id=self.website.id,
                price=item.get("price"),
                original_price=item.get("original_price", None),
                discount=discount,
                url=item.get("url"),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            .on_conflict_do_update(
                index_elements=["url"],
                set_=dict(
                    price=item.get("price"), updated_at=datetime.now(timezone.utc)
                ),
            )
            .returning(Deal)
        )

        deal = self.session.execute(stmt)
        try:
            self.session.commit()
        except Exception as e:
            print(f"Failed to upsert deal: {e}")
            self.session.rollback()

        return deal.scalars().one()

    def process_item(self, item, spider) -> Deal:
        """
        Validate item, upsert product and deal info to database
        """
        self.validate(item)

        # Insert product details
        product = self.upsert_product(item)

        # Insert deal details
        deal = self.upsert_deal(item, product)
        return deal


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


def get_brand(title: str) -> str | None:
    """
    Helper function to get brand from title if it can't be scraped

    Args:
      title: Product title
      start_tags: Product tags pulled from url

    Returns:
      List[str]: list of all tags
    """
    # Get keyword --> tag map
    json_path = Path(__file__).parent.parent / "expressions" / "brands.json"
    keywords = read_json(json_path)
    title = title.lower()

    for kw in keywords.keys():
        if kw in title:
            return keywords[kw]
