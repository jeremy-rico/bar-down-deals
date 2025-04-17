import json
import math
import subprocess
import sys

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import Executable

from src.core.config import settings
from src.core.database import get_session
from src.deals.models import Deal
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


def get_headers(data: list[Deal], limit: int) -> dict[str, str]:
    # Generate response headers
    avail_brands = set()
    avail_tags = set()
    avail_stores = set()
    avail_sizes = set()
    ret_max_price = 0.0
    sizes = ["Senior", "Intermediate", "Junior", "Youth", "Adult", "Womens"]
    import sys

    print(sys.getsizeof(data))
    for row in data:
        if row.product.brand:
            avail_brands.add(row.product.brand)
        if row.product.categories:
            for cat in row.product.categories:
                if cat.name in sizes:
                    avail_sizes.add(cat.name)
                else:
                    avail_tags.add(cat.name)
        if row.website.name:
            avail_stores.add(row.website.name)
        ret_max_price = max(ret_max_price, row.price)

    headers = {
        "x-total-item-count": len(data),
        "x-items-per-page": limit,
        "x-total-page-count": math.ceil(len(data) / limit),
        "x-avail-sizes": json.dumps(list(avail_sizes)),
        "x-avail-brands": json.dumps(list(avail_brands)),
        "x-avail-tags": json.dumps(list(avail_tags)),
        "x-avail-stores": json.dumps(list(avail_stores)),
        "x-max-price": ret_max_price,
    }
    return headers
