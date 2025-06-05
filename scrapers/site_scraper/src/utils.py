import json
import logging
import re
import sys
from pathlib import Path

from api.src.currencies.models import ExchangeRate
from sqlmodel import col, select

from scrapers.site_scraper.src.database import get_session
from scrapers.site_scraper.src.settings import LOG_LEVEL


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


def convert_to_usd(amount: float, base_currency: str) -> float:

    session = get_session()
    stmt = select(col(ExchangeRate.rate)).where(
        ExchangeRate.target_currency == base_currency
    )

    result = session.execute(stmt)
    rate = result.scalar()
    if not rate:
        raise ValueError(f"No rate found for {base_currency}")

    return round(amount * (1 / float(rate)), 2)
