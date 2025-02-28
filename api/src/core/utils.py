import os
import subprocess
import sys

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.core.database import get_session
from src.products.models import Category


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


async def populate_categories(
    categories: list[str],
) -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        try:
            for category in categories:
                stmt = (
                    insert(Category)
                    .values(name=category)
                    .on_conflict_do_nothing(index_elements=["name"])
                    .returning(Category)
                )
                await session.execute(stmt)
                await session.commit()
            print("Categories populated.")

        except Exception as e:
            print(f"An error occurred while populating categories: {e}")

        await session.close()
