# do stuff
import argparse

from core.alerts import send_alerts

parser = argparse.ArgumentParser(
    prog="BDD Email Alert Bot",
    description="""A bot to send nightly, weekly, or monthly emails to users
    who have signed up for category or keyword alerts""",
)
parser.add_argument(
    "-g",
    "--group",
    choices=["nightly", "weekly", "monthly"],
    help="Which user group to send alerts to.",
)


def main() -> None:
    args = parser.parse_args()
    send_alerts(args.group)


if __name__ == "__main__":
    main()
