import json
import re
from pathlib import Path


def clean_price(s: str) -> str | None:
    """
    Uses regular expression to find the first match of a floating point in the
    string

    Args:
        s: price string as scraped by spider

    Returns:
        str: re match
    """

    match = re.search(r"\d+.\d\d", s)
    if match:
        return match.group(0)


def clean_brand(s: str):
    """
    Clean scraped brand string
    """
    if s.lower().startswith("by"):
        return s.split()[-1]
    return s


def get_discount(salePrice: float, originalPrice: float | None) -> float | None:
    if not originalPrice:
        return None
    salePrice, originalPrice = float(salePrice), float(originalPrice)
    return (originalPrice - salePrice) / originalPrice * 100


def read_json(jsonPath: Path) -> dict:
    with open(str(jsonPath)) as f:
        return json.load(f)
