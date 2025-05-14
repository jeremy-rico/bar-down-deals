import smtplib
import subprocess
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.core.database import DATABASE_URL, get_session
from src.deals.models import Deal
from src.products.models import Tag


def run_migrations():
    """
    Runs Alembic database migrations using sys.executable and module execution.

    This method is more compatible with environments like Vercel where direct
    command execution might be restricted.
    """
    try:
        # Ensure the current directory is in the Python path
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # sys.path.insert(0, current_dir)

        # Use sys.executable to run the Alembic module
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Print the output if there's any
        if result.stdout:
            print("Migration output:", result.stdout)

        print("Migrations completed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Migration failed. Error: {e}")
        print("Standard output:", e.stdout)
        print("Standard error:", e.stderr)
        raise
    except Exception as e:
        print(f"An error occurred while running migrations: {e}")
        raise


async def populate_tags(
    tags: list[str],
) -> None:
    engine = create_async_engine(DATABASE_URL, echo=False, future=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        try:
            for tag in tags:
                stmt = (
                    insert(Tag)
                    .values(name=tag)
                    .on_conflict_do_nothing(index_elements=["name"])
                    .returning(Tag)
                )
                await session.execute(stmt)
                await session.commit()
            print("Tags populated.")

        except Exception as e:
            print(f"An error occurred while populating categories: {e}")

        finally:
            await session.close()


async def send_reset_email(to_email: str, reset_link: str) -> None:
    # Email credentials
    SMTP_SERVER = settings.EMAIL_HOST
    SMTP_PORT = settings.EMAIL_PORT
    FROM_EMAIL = settings.EMAIL_USER
    FROM_PASSWORD = settings.EMAIL_PASSWORD

    # Create email content
    subject = "Password Reset Request"
    text = f"Hi,\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you did not request this, please ignore this email."
    html = f"""
    <html>
      <body>
        <p>Hi!<br><br>
           A password reset was requested for your BarDownDeals account.<br>
           <a href="{reset_link}">Click here to reset your password!</a><br><br>
           This link will expire in <strong>ten minutes</strong>. <br><br>
           If you did not request this, you may safely ignore this email.
        </p>
      </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = FROM_EMAIL
    message["To"] = to_email

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    # Send the email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, FROM_PASSWORD)
            server.sendmail(FROM_EMAIL, to_email, message.as_string())
            print(f"Reset email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
