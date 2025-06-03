import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from api.src.sticks.models import Stick, StickPrice
from sqlmodel import col, func, select

from scrapers.stick_scraper.src.database import get_session
from scrapers.stick_scraper.src.logging import get_logger

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
        float: discount percentage
        None: if no original_price
    """
    if not original_price:
        return None
    sale_price, original_price = float(sale_price), float(original_price)
    return (original_price - sale_price) / original_price * 100


def read_json(jsonPath: Path) -> dict:
    with open(str(jsonPath)) as f:
        return json.load(f)


def update_sticks() -> None:
    """
    Update stick timestamp, price, price_drop, and historical_price cols
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
            select(func.min(StickPrice.price).label("price"), StickPrice.currency)
            .where(StickPrice.stick_id == stick.id, StickPrice.timestamp >= since)
            .group_by(col(StickPrice.stick_id), col(StickPrice.currency))
        )
        result = session.execute(stmt)
        latest_price = result.one_or_none()

        if not latest_price:
            logger.warning(f"No price for stick {stick.id} in the last 24 hrs")
            continue

        latest_price = {"price": latest_price[0], "currency": latest_price[1]}

        # Convert currency if necessary
        if latest_price["currency"] != stick.currency:
            latest_price["price"] = convert_currency(
                latest_price["price"], latest_price["currency"], stick.currency
            )

        if latest_price["price"] < stick.price:
            # Set price drop
            stick.price_drop = True

            # Get historical low price
            stmt = (
                select(func.min(StickPrice.price).label("price"), StickPrice.currency)
                .where(StickPrice.stick_id == stick.id)
                .group_by(col(StickPrice.stick_id), col(StickPrice.currency))
            )
            result = session.execute(stmt)
            historical_low_price = result.one()

            historical_low_price = {
                "price": historical_low_price[0],
                "currency": historical_low_price[1],
            }

            # Convert currency if necessary
            if historical_low_price["currency"] != latest_price["currency"]:
                historical_low_price["price"] = convert_currency(
                    historical_low_price["price"],
                    historical_low_price["currency"],
                    latest_price["currency"],
                )

            # Set historical low bool
            stick.historical_low = latest_price["price"] < historical_low_price["price"]

            stick.price = latest_price["price"]
            stick.currency = latest_price["currency"]
            logger.info(f"Found new price for stick {stick.id}")
        else:
            stick.price_drop = False

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


def convert_currency(amount: float, from_curr: str, to_curr: str) -> float:
    """
    Real time currency conversion
    """
    url = f"https://api.exchangerate.host/convert"
    params = {"from": from_curr, "to": to_curr, "amount": amount}

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200 and data.get("success"):
        result = data["result"]
        print(f"{amount} {from_curr} = {result:.2f} {to_curr}")
        return result
    else:
        raise Exception("Currency conversion failed.")
