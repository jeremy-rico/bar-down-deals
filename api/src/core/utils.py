import subprocess
import sys
from decimal import Decimal

import requests
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.core.database import DATABASE_URL, get_session
from src.deals.models import Deal
from src.products.models import Tag


async def convert_currency(amount: Decimal, from_curr: str, to_curr: str) -> Decimal:
    """
    Real time currency conversion
    """
    api_key = settings.EXCHANGERATE_API_KEY
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_curr}/{to_curr}/{amount}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and data.get("result") == "success":
        conversion_result = data.get("conversion_result")
        return round(conversion_result, 2)
    else:
        raise Exception("Currency conversion failed.")


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
