import logging
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin, urlparse

import boto3
from api.src.alerts.models import UserAlert
from api.src.deals.models import Deal
from api.src.products.models import Product  # Need this to resolve Deal model
from api.src.users.models import Users
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session
from sqlmodel import col, delete, func, select

from scrapers.site_scraper.src.logging import get_logger
from scrapers.site_scraper.src.settings import DATABASE_URL, S3_HOST

logger = get_logger(__name__)


# Create engine
engine = create_engine(DATABASE_URL, echo=False, future=True)


def get_session() -> Session:
    """
    Dependency for getting database session.

    Yields:
        Session: Database session
    """

    # Create session
    return Session(engine)


def clean_database() -> None:
    """
    After nightly scrape, remove deals that haven't been updated in 48 hrs. This means
    its hasn't been found for two crawls and is probably removed from the parent site.
    """

    logger.info("Cleaning database...")
    session = get_session()
    expiration = datetime.now(timezone.utc) - timedelta(days=2)

    stmt = delete(Deal).filter(col(Deal.updated_at) <= expiration)
    count = (
        session.query(func.count())
        .select_from(Deal)
        .filter(col(Deal.updated_at) <= expiration)
        .scalar()
    )

    try:
        session.execute(stmt)
        session.commit()
        logger.info(f"Successfully removed {count} deals.")
    except Exception as e:
        logger.critical(f"Failed to clean database: {e}")
        session.rollback()


def clean_bucket(
    bucket_name: str = "bar-down-deals-bucket",
    prefix: str = "images/full/",
):
    """
    Delete images no longer in the database

    Args:
        bucket_name: name of bucket
        prefix: path to directory to clean

    Returns:
        None
    """
    session = get_session()
    logging.getLogger("botocore").setLevel(logging.CRITICAL)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)
    logger.info(f"Deleting unused images from {bucket_name}")
    count = 0
    try:
        s3 = boto3.client("s3")

        paginator = s3.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        for page in page_iterator:
            if "Contents" in page:
                for obj in page["Contents"]:
                    base_url = ("/").join(S3_HOST.split("/")[:-1])
                    obj_url = urljoin(base_url, obj["Key"])
                    stmt = select(Product).where(Product.image_url == obj_url)
                    if session.scalar(stmt) is None:
                        count += 1
                        s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
                        # logging.debug(f"Deleted {obj['Key']}")

        logging.info("Successfully cleaned bucket!")
        logging.debug(f"Deleted {count} objects")
    except Exception as e:
        logging.critical(f"Failed to clean s3 bucket: {e}")
