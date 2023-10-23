import logging
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.INFO)
load_dotenv(".env", verbose=True)


class Settings(BaseSettings):
    """App settings."""

    PROJECT_NAME: str = "todo_fastapi"

    # データベース
    DB_USER: str | None = os.getenv("DB_USER")
    DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")
    DB_HOST: str = "db"
    DB_PORT: str = "5432"
    DB_NAME: str = os.getenv("DB_NAME")

    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    model_config = SettingsConfigDict(
        case_sensitive=True,
    )


settings = Settings()
