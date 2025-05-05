# do stuff
import argparse

from alerts.src.core.alerts import AlertBot
from alerts.src.core.logging import setup_logging

parser = argparse.ArgumentParser(
    prog="BDD Email Alert Bot",
    description="""A bot to send nightly, weekly, or monthly emails to users
    who have signed up for category or keyword alerts""",
)
parser.add_argument(
    "-f",
    "--frequency",
    choices=["daily", "weekly", "monthly"],
    help="Which user group to send alerts to.",
)


setup_logging()


def main() -> None:
    args = parser.parse_args()
    alert_bot = AlertBot()
    alert_bot.send_alerts(args.group)


if __name__ == "__main__":
    main()
