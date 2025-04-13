import logging
from datetime import datetime, timedelta, timezone

import boto3
from api.src.deals.models import Deal
from api.src.products.models import Product  # Need this to resolve Deal model
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session
from sqlmodel import col, delete


def get_session(database_url: URL) -> Session:
    """
    Dependency for getting database session.

    Yields:
        Session: Database session
    """
    # Create engine
    engine = create_engine(database_url, echo=False, future=True)

    # Create session
    return Session(engine)


def clean_database(database_url: URL) -> None:
    """
    After nightly scrape, remove deals that are over 48 hrs old. This means they
    haven't been scraped twice in a row and are probably removed from the parent
    site.

    """

    logging.info("Cleaning database...")
    session = get_session(database_url)
    expiration = datetime.now(timezone.utc) - timedelta(days=2)

    stmt = delete(Deal).filter(col(Deal.updated_at) <= expiration)

    try:
        session.execute(stmt)
        session.commit()
        logging.info("Successfully cleaned database.")
    except Exception as e:
        logging.critical(f"Failed to clean database: {e}")
        session.rollback()


def clean_bucket(
    bucket_name: str = "bar-down-deals-bucket",
    prefix: str = "images/full/",
    days_inactive: int = 7,
):
    """
    Auto delete objects if not modified for seven days

    Args:
        bucket_name: name of bucket
        prefix: path to directory to clean
        days_inactive: days of inactivity

    Returns:
        None
    """
    logging.info(
        f"Deleting objects older than {days_inactive} days from bucket {bucket_name}"
    )
    count = 0
    try:
        s3 = boto3.client("s3")
        threshold_date = datetime.now(timezone.utc) - timedelta(days=2)

        paginator = s3.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        for page in page_iterator:
            if "Contents" in page:
                for obj in page["Contents"]:
                    last_modified = obj["LastModified"]

                    if last_modified > threshold_date:
                        count += 1
                        logging.debug(
                            f"Deleting {obj['Key']} last modified on {last_modified}"
                        )
                        s3.delete_object(Bucket=bucket_name, Key=obj["Key"])

        logging.info("Successfully cleaned bucket!")
        logging.info(f"Deleted {count} objects")
    except Exception as e:
        logging.critical(f"Failed to clean s3 bucket: {e}")
