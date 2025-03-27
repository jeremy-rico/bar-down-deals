from pydantic_settings import BaseSettings
from sqlalchemy import URL

from src.aws.utils import get_ssm_param


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = "Bar Down Deals API"
    DATABASE_URL: URL = URL.create(
        drivername="postgresql+asyncpg",
        username=get_ssm_param("DB_USER", "postgres"),
        password=get_ssm_param("DB_PASSWORD", "", secure=True),
        host=get_ssm_param("DB_HOST", "localhost"),
        port=get_ssm_param("DB_PORT", "5432"),
        database=get_ssm_param("DB_NAME", "postgres"),
    )
    DEBUG: bool = False
    ORIGINS: list[str] = [
        "http://localhost:3000"
    ]

    # JWT Settings
    JWT_SECRET: str = "test"  # TODO: Change in production
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 30  # minutes

    # # TODO: Remove this? No need for .env file
    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     env_file_encoding="utf-8",
    # )

    CATEGORIES: list[str] = [
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
        # Sizing
        "Senior",
        "Intermediate",
        "Junior",
        "Youth",
        # Stick Type
        "Composite",
        "Street",
        "Wooden",
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


settings = Settings()
