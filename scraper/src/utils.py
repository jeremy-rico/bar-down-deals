import json
import logging
import re
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path

from scraper.src.settings import (
    EMAIL_HOST,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_USER,
    LOG_LEVEL,
)


def setup_logging() -> None:
    """Set up logging configuration."""
    format_string = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "CRITICAL": logging.CRITICAL,
    }
    logging.basicConfig(
        level=log_level_map[LOG_LEVEL],
        format=format_string,
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)


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


def send_email(to: str, subject: str, body: str) -> None:
    """
    Send alerts to users who have signed up for keyword alerts.

    Args:
        to: email address to send to
        subject: email subject string
        body: email body string

    Returns:
        None

    Raises:
        Generic Exception: email failed to send
    """

    # Your Zoho email credentials
    smtp_server = EMAIL_HOST
    smtp_port = EMAIL_PORT
    username = EMAIL_USER
    password = EMAIL_PASSWORD

    # Email details
    from_email = username
    to_email = to
    subject = subject
    body = body

    # Create email message
    msg = MIMEMultipart()
    msg["From"] = formataddr(("BarDownDeals", from_email))
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Use .starttls() for TLS
            server.login(username, password)
            server.send_message(msg)
            print(f"Email successfully sent to {to}.")
    except Exception as e:
        print(f"Failed to send email: {e}")
