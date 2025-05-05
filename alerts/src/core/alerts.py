import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path
from pprint import pprint

import requests
from api.src.alerts.models import UserAlert
from api.src.deals.models import Deal
from api.src.products.models import Product, Tag
from api.src.users.models import Users  # needed for UserAlert to resolve
from jinja2 import Environment, FileSystemLoader
from sqlmodel import select

from alerts.src.core.config import settings
from alerts.src.core.database import get_session
from alerts.src.core.logging import get_logger
from alerts.src.core.utils import read_json

logger = get_logger(__name__)

tags = read_json(Path(__file__).parent.parent.parent.parent / "api/src/core/tags.json")
template_path = Path(__file__).parent.parent / "templates"


class AlertBot:
    def __init__(self):
        self.session = get_session()
        self.logo_url = "https://bar-down-deals-bucket.s3.us-west-1.amazonaws.com/images/logo/email_logo.png"
        self.api = "https://api.bardowndeals.com/"
        self.added_since_map = {"daily": "today", "weekly": "week", "monthly": "month"}

    def send_alerts(self, frequency: str):

        # Get all weekly alerts
        stmt = (
            select(UserAlert.user_id).where(UserAlert.frequency == frequency).distinct()
        )

        # Get all users subscribed to weekly alerts
        user_ids = self.session.scalars(stmt)

        for user_id in user_ids:
            # Get all alerts for user
            stmt = select(UserAlert.keyword).where(UserAlert.user_id == user_id)
            user_tags = list(self.session.scalars(stmt))

            # Get all deal data
            deals_map = self.get_data(
                user_tags=user_tags, added_since=self.added_since_map[frequency]
            )

            # Render email body using data
            alert_body = self.render_alert(
                template_path=str(template_path),
                frequency=frequency,
                deals_map=deals_map,
                logo_url=self.logo_url,
            )

            # Get user email
            stmt = select(Users.email).where(Users.id == user_id)
            user_email = self.session.execute(stmt).one()[0]

            # Send email
            self.send_alert(
                to=user_email,
                subject=f"Your {frequency} deal alerts",
                body=alert_body,
            )

    def get_data(self, user_tags: list[str], added_since: str) -> dict:
        """
        Uses BarDownDeals api to grab relevent deals
        """
        deals_map = {}
        stmt = select(Tag)
        all_tags = self.session.scalars(stmt).all()

        stmt = select(Product.brand).distinct()
        brands = self.session.scalars(stmt).all()

        for user_tag in user_tags:
            if user_tag.title() in all_tags:
                response = requests.get(
                    self.api
                    + f"deals/?added_since={added_since}&tags={user_tag.title()}"
                )
                data = response.json()
            elif user_tag.title() in brands:
                response = requests.get(
                    self.api
                    + f"deals/?added_since={added_since}&brands={user_tag.title()}"
                )
                data = response.json()
            else:
                response = requests.get(
                    self.api + f"search/?added_since={added_since}&q={user_tag}"
                )
                data = response.json()

            deals_map[user_tag] = data
        return deals_map

    def render_alert(
        self,
        template_path: str,
        frequency: str,
        deals_map: dict,
        logo_url: str,
    ):
        """
        Render email html using jinja2 injection
        """
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template("email_template.html")
        return template.render(
            frequency=frequency,
            deals_map=deals_map,
            logo_url=logo_url,
        )

    def send_alert(self, to: str, subject: str, body: str) -> None:
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
        smtp_server = settings.EMAIL_HOST
        smtp_port = int(settings.EMAIL_PORT)
        username = settings.EMAIL_USER
        password = settings.EMAIL_PASSWORD

        # Email details
        from_email = username
        to_email = to
        subject = subject
        body = body

        # Create email message
        msg = MIMEText(body, "html")
        msg["From"] = formataddr(("BarDownDeals", from_email))
        msg["To"] = to_email
        msg["Subject"] = subject

        try:
            # Connect and send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Use .starttls() for TLS
                server.login(username, password)
                server.send_message(msg)
                print(f"Email successfully sent to {to}.")
        except Exception as e:
            print(f"Failed to send email: {e}")
