from pydantic_settings import BaseSettings  # , SettingsConfigDict
from sqlalchemy import URL

from utils.aws import get_ssm_param


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

    # JWT Settings
    JWT_SECRET: str = "test"  # TODO: Change in production
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 30  # minutes

    # # TODO: Remove this? No need for .env file
    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     env_file_encoding="utf-8",
    # )


settings = Settings()
