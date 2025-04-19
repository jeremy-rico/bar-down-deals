import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

print(os.environ)


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = "Bar Down Deals API"
    DB_DRIVERNAME: str = "postgresql+asyncpg"
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    FRONTEND_KEY: str

    DEBUG: bool = False
    ORIGINS: list[str] = [
        "http://localhost:3000",
        "https://bardowndeals.com",
        "https://www.bardowndeals.com",
    ]

    # JWT Settings
    JWT_SECRET: str = "test"  # TODO: Change in production
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 30  # minutes

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()

DATABASE_URL = URL.create(
    drivername=settings.DB_DRIVERNAME,
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)

TAGS: list[str] = [
    # Get Sizing
    "Senior",
    "Intermediate",
    "Junior",
    "Youth",
    # Major Categories
    "Sticks",
    "Skates",
    "Protective",
    "Gamewear",
    "Bags",
    "Roller",
    "Goalie",
    "Apparel",
    "Accessories",
    # Stick Type
    "Composite",
    "Street",
    "Wood",
    # Protective
    "Helmets",
    "Cages & Shields",
    "Gloves",
    "Shoulder Pads",
    "Shin Guards",
    "Elbow Pads",
    "Pants",
    "Pant Shells",
    "Jocks",
    "Base Layer",
    # Goalie
    "Leg Pads",
    "Masks",
    "Blockers",
    "Chest & Arm",
    "Knee Protectors",
    "Catchers",
    "Goalie Sticks",
    "Goalie Skates",
    # Roller
    "Inline Skates",
    "Inline Wheels",
    "Inline Pants",
    # Apparel Sizing
    "Adult",
    "Womens",
    "Headwear",
    # Savings
    "Coupons",
    "Promos",
]
