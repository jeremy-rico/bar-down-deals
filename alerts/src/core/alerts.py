import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path
from pprint import pprint
from urllib.parse import urlencode

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

template_path = Path(__file__).parent.parent / "templates"


class AlertBot:
    def __init__(self):
        self.session = get_session()
        self.logo_url = "https://bar-down-deals-bucket.s3.us-west-1.amazonaws.com/images/logo/email_logo.png"
        self.api = "https://api.bardowndeals.com/"
        self.added_since_map = {"daily": "today", "weekly": "week"}
        self.success = 0
        self.fail = 0

    def send_alerts(self, frequency: str):

        # Get all unique user ids for alert frequency
        stmt = (
            select(UserAlert.user_id).where(UserAlert.frequency == frequency).distinct()
        )
        user_ids = self.session.scalars(stmt)

        for user_id in user_ids:
            # Get all alerts for user
            stmt = select(UserAlert).where(UserAlert.user_id == user_id)
            user_alerts = list(self.session.scalars(stmt))

            # Get all deal data
            deals_map = self.get_data(user_alerts=user_alerts)

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

        results = {
            "Total": self.success + self.fail,
            "Success": self.success,
            "Failed": self.fail,
        }
        logger.info(f"Finished sending alerts.")
        for k, v in results.items():
            logger.info(f"{k}: {v}")

    def get_data(self, user_alerts: list[UserAlert]) -> dict:
        """
        Uses BarDownDeals api to grab relevent deals
        """
        deals_map = {}

        for user_alert in user_alerts:
            title = self.build_title(user_alert)
            url = self.build_url(user_alert)
            response = requests.get(url)
            new_data = response.json()

            # if no new deals
            if not new_data:
                url = self.build_url(user_alert, added_since=False)
                response = requests.get(url)
                data = response.json()
                deals_map[title] = {"new_count": 0, "deals": data}
            else:
                deals_map[title] = {"new_count": len(new_data), "deals": new_data}

        return deals_map

    def build_url(self, user_alert: UserAlert, added_since=True) -> str:
        """
        Build api endpoint using alert data
        """
        endpoint = "search/?" if user_alert.keyword else "deals/?"
        params = []
        params.append(("sort", "Newest"))
        params.append(("limit", 10))

        for tag in [user_alert.tag, user_alert.size]:
            if tag:
                params.append(("tags", tag))

        if user_alert.brand:
            params.append(("brands", user_alert.brand))

        if user_alert.keyword:
            params.append(("q", user_alert.keyword))

        if added_since:
            params.append(("added_since", self.added_since_map[user_alert.frequency]))

        query_string = urlencode(params, doseq=True)
        return self.api + endpoint + query_string

    def build_title(self, user_alert: UserAlert) -> str:
        """
        Build alert title
        """
        title = []

        if user_alert.size:
            title.append(user_alert.size)
        if user_alert.brand:
            title.append(user_alert.brand)
        if user_alert.tag:
            title.append(user_alert.tag)
        if user_alert.keyword:
            title.append(user_alert.keyword)

        return "+".join(title)

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
                logger.info(f"Successfully sent alert to {to}.")
            self.success += 1
        except Exception as e:
            self.fail += 1
            logger.critical(f"Failed to send alert to {to}: {e}")
