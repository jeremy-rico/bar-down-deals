from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    """
    Application settings. If no default value is provided, the value must be
    loaded from a .env file
    """

    PROJECT_NAME: str = "Bar Down Deals Alert Bot"

    # Database settings
    DB_DRIVERNAME: str = "postgresql"
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # SMTP server settings
    EMAIL_HOST: str
    EMAIL_PORT: str
    EMAIL_USER: str
    EMAIL_PASSWORD: str

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "CRITICAL"] = "DEBUG"

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
