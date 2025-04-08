import logging
from datetime import datetime, timedelta, timezone

import boto3


def get_ssm_param(name, default="", secure=False) -> str:
    """
    Fetch parameters from AWS SSM parameter store

    Args:
        name: name of ssm param
        secure: bool if ssm param is encrypted

    Returns:
        Value of ssm param
    """
    ssm = boto3.client("ssm", region_name="us-west-1")
    try:
        param = ssm.get_parameter(Name=name, WithDecryption=secure)
        return param["Parameter"]["Value"]
    except:
        return default


# TODO: Put this in a lambda function and run every 24 hours
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
    logging.getLogger().setLevel(logging.INFO)
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


if __name__ == "__main__":
    clean_bucket()
