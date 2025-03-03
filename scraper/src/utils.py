import json
from pathlib import Path
from urllib.parse import urlparse


def clean_price(s: str):
    """
    Remove dollar symbol from string
    """
    if s.startswith("$"):
        return s[1 : len(s)]
    return s


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
