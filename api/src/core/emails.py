import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from src.core.config import settings
from src.core.logging import get_logger

logo_url = "https://bar-down-deals-bucket.s3.us-west-1.amazonaws.com/images/logo/email_logo.png"
template_path = Path(__file__).parent / "templates"
logger = get_logger(__name__)


async def send_welcome_email(to: str) -> None:
    # Email credentials
    SMTP_SERVER = settings.EMAIL_HOST
    SMTP_PORT = settings.EMAIL_PORT
    FROM_EMAIL = settings.EMAIL_USER
    EMAIL_PASSWORD = settings.EMAIL_PASSWORD

    # Render email body
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("welcome_template.html")
    body = template.render(
        logo_url=logo_url,
        email=to,
    )

    # Setup email
    msg = MIMEText(body, "html")
    msg["From"] = formataddr(("BarDownDeals", FROM_EMAIL))
    msg["To"] = to
    msg["Subject"] = "Welcome to BarDownDeals!"

    # Send email
    try:
        # Connect and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Use .starttls() for TLS
            server.login(FROM_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
            logger.info(f"Successfully sent welcome email to {to}.")
    except Exception as e:
        logger.critical(f"Failed to send welcome email to {to}: {e}")


async def send_reset_email(to: str, reset_link: str) -> None:
    # Email credentials
    SMTP_SERVER = settings.EMAIL_HOST
    SMTP_PORT = settings.EMAIL_PORT
    FROM_EMAIL = settings.EMAIL_USER
    EMAIL_PASSWORD = settings.EMAIL_PASSWORD

    # Render email body
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("reset_template.html")
    body = template.render(
        logo_url=logo_url,
        reset_link=reset_link,
    )

    # Setup email
    msg = MIMEText(body, "html")
    msg["From"] = formataddr(("BarDownDeals", FROM_EMAIL))
    msg["To"] = to
    msg["Subject"] = "Password Reset"

    # Send email
    try:
        # Connect and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Use .starttls() for TLS
            server.login(FROM_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
            logger.info(f"Successfully sent reset email to {to}.")
    except Exception as e:
        logger.critical(f"Failed to send reset email to {to}: {e}")
