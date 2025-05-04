import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from core.logging import get_logger

logger = get_logger(__name__)


def send_alerts(group: str):
    if group == "nightly":
        # Step 1:
        # alerts = select(UserAlerts).where(UserAlerts.freq == "nightly")
        # Step 2:
        # For each UserAlert
        #   if alert.keyword in categories
        #       send all deals of that category from the last 24 hrs
        #   else:
        #       search for keyword
        #       Send results from last 24 hrs
        logger.info("Sending nightly alerts...")
    elif group == "weekly":
        logger.info("Sending weekly alerts")
    elif group == "monthly":
        logger.info("Sending monthly alerts")


def send_alert(to: str, subject: str, body: str) -> None:
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
