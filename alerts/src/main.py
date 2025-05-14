import argparse
from datetime import datetime, timezone

from alerts.src.core.alerts import AlertBot
from alerts.src.core.logging import get_logger, setup_logging

parser = argparse.ArgumentParser(
    prog="BDD Email Alert Bot",
    description="""A bot to send nightly, weekly, or monthly emails to users
    who have signed up for category or keyword alerts""",
)
parser.add_argument(
    "-f",
    "--frequency",
    choices=["daily", "weekly"],
    help="Which user group to send alerts to.",
)


setup_logging()
logger = get_logger(__name__)


def main() -> None:
    args = parser.parse_args()
    logger.info(f"Sending {args.frequency} alerts.")

    start = datetime.now(timezone.utc)
    logger.info(f"Start time: {start} UTC")

    alert_bot = AlertBot()
    alert_bot.send_alerts(args.frequency)

    time_elapsed = datetime.now(timezone.utc) - start
    logger.info(f"All processes completed in {time_elapsed.total_seconds()} seconds")


if __name__ == "__main__":
    main()
