import subprocess
import sys
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.core.config import settings
from src.currencies.models import ExchangeRate


async def convert_currency(
    session: AsyncSession, amount_usd: Decimal, target_currency: str
) -> Decimal:
    """
    Converts specified amount from USD to target currency
    """

    if target_currency == "USD":
        return round(amount_usd, 2)

    if target_currency not in settings.SUPPORTED_CURRENCIES:
        raise HTTPException(
            status_code=400, detail=f"Unsupported currency: {target_currency}"
        )

    stmt = select(ExchangeRate).where(
        ExchangeRate.base_currency == "USD",
        ExchangeRate.target_currency == target_currency,
    )
    result = await session.execute(stmt)
    rate_obj = result.scalars().first()

    if not rate_obj:
        raise HTTPException(status_code=503, detail="Exchange rate not available")

    return Decimal(round(amount_usd * rate_obj.rate, 2))


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
