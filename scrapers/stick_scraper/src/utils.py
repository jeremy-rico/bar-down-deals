import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from api.src.currencies.models import ExchangeRate
from api.src.deals.models import Website  # need because StickPrice
from api.src.products.models import Product  # need because Website
from api.src.sticks.models import Stick, StickPrice, StickURL
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import col, func, select

from scrapers.stick_scraper.src.database import get_session
from scrapers.stick_scraper.src.logging import get_logger
from scrapers.stick_scraper.src.settings import EXCHANGERATE_API_KEY

logger = get_logger(__name__)


def clean_price(s: str) -> str | None:
    """
    Uses regular expression to find the first match of a floating point in the
    string

    Args:
        s: price string as scraped by spider

    Returns:
        str: re match
    """

    # re explanation:
    # \d: any number of digits
    # (,\d{3})?: optional comma and exactly three digits
    # .\d{2}: exactly decimal and two digits
    match = re.search(r"\d+(,\d{3})?\.\d\d?", s)
    if match:
        s = match.group(0)
        match = re.search(r"\.\d$", s)
        if match:
            s += "0"
        return "".join(s.split(",")) if "," in s else s


def clean_brand(s: str):
    """
    Clean scraped brand string
    """
    if s.lower().startswith("by"):
        return s.split()[-1]
    return s


def get_discount(sale_price: float, original_price: float | None) -> float | None:
    """
    Calculate discount

    Args:
        sale_price: final/sale price of the item
        original_price: original price of the item

    Returns:
        float: discount percentage, rounded to two decimal places
        None: if no original_price
    """
    if not original_price:
        return None
    sale_price, original_price = float(sale_price), float(original_price)
    return round((original_price - sale_price) / original_price * 100, 2)


def read_json(jsonPath: Path) -> dict:
    with open(str(jsonPath)) as f:
        return json.load(f)


def update_sticks() -> None:
    """
    Update stick timestamp, price, price_drop, and historical_price after
    scrape. This is done here because it will also RAISE the price if a sale
    ends. No need for currency conversion here. All prices are stored in USD.

    Note: Sticks stay in a price drop and historical low state UNTIL the price
    rises. As long as the price remains stead or goes down, it will stay in this
    state.
    """
    # Get db session
    session = get_session()

    # Get all sticks
    stmt = select(Stick).distinct()
    result = session.execute(stmt)
    sticks = result.scalars().all()

    # Define time scale
    since = datetime.now(timezone.utc) - timedelta(days=1)

    for stick in sticks:
        # Get lowest price in last 24 hrs
        stmt = (
            select(func.min(StickPrice.price).label("price"))
            .where(StickPrice.stick_id == stick.id, StickPrice.timestamp >= since)
            .group_by(col(StickPrice.stick_id))
        )
        result = session.execute(stmt)
        latest_price = result.scalar_one_or_none()

        if not latest_price:
            logger.warning(f"No price for stick {stick.id} in the last 24 hrs")
            continue

        if latest_price < stick.price:
            # Set price drop
            stick.price_drop = True

            # Check if price drop is historical low
            stmt = (
                select(func.min(StickPrice.price).label("price"))
                .where(StickPrice.stick_id == stick.id)
                .group_by(col(StickPrice.stick_id))
            )
            result = session.execute(stmt)
            historical_low_price = result.scalar()

            # Set historical low
            if latest_price < historical_low_price:
                stick.historical_low = True

            logger.info(f"Found new price {latest_price} for stick {stick.id}")
        elif latest_price > stick.price:
            # Reset if price increased
            stick.price_drop = False
            stick.historical_low = False

        stick.price = latest_price
        stick.discount = round((stick.msrp - stick.price) / stick.msrp * 100, 2)
        stick.updated_at = datetime.now(timezone.utc)

        session.add(stick)
        try:
            session.commit()
            session.refresh(stick)
            logger.info(f"Updated stick {stick.id}")
        except Exception as e:
            logger.critical(f"Failed to update stick {stick.id}: {e}")
            session.rollback()

    return


def fetch_usd_exchange_rates() -> None:
    """
    Get exchange rates after nightly scrapes. This function has basically
    nothing to do with the scraper. It shouldn't be here, but since I'm running
    it right after both scrapers have completed, here it stays :)

    """
    session = get_session()
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/latest/USD"
    res = requests.get(url)
    data = res.json()
    if res.status_code == 200 and data.get("result") == "success":
        for currency, rate in data.get("conversion_rates").items():
            stmt = (
                insert(ExchangeRate)
                .values(
                    base_currency="USD",
                    target_currency=currency,
                    rate=rate,
                    timestamp=datetime.now(timezone.utc),
                )
                .on_conflict_do_update(
                    index_elements=["target_currency"],
                    set_=dict(rate=rate, timestamp=datetime.now(timezone.utc)),
                )
                .returning(ExchangeRate)
            )
            session.execute(stmt)
            try:
                session.commit()
            except Exception as e:
                logger.warning(f"Failed to upsert exchange rate: {e}")
                session.rollback()


def convert_to_usd(amount: float, base_currency: str) -> float:
    """
    Convert foreign currency to USD
    """

    session = get_session()
    stmt = select(col(ExchangeRate.rate)).where(
        ExchangeRate.target_currency == base_currency
    )

    result = session.execute(stmt)
    rate = result.scalar()
    if not rate:
        raise ValueError(f"No rate found for {base_currency}")

    return round(amount * (1 / float(rate)), 2)


def get_urls(spider_name: str) -> dict[str, int]:
    """
    Get urls for spider to scrape stored in db

    Args:
        spider_name: str

    Returns:
        dict: url, stick_id
    """

    session = get_session()
    stmt = select(StickURL).where(StickURL.spider_name == spider_name)
    result = session.execute(stmt)
    stick_urls = result.scalars().all()
    return {stick_url.url: stick_url.stick_id for stick_url in stick_urls}
