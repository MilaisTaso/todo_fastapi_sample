import logging
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.INFO)
load_dotenv(".env", verbose=True)


class Settings(BaseSettings):
    """App settings."""

    RUN_ENV: str | None = os.getenv("RUN_ENV")
    PROJECT_NAME: str = "todo_fastapi"
    DEBUG: bool = True

    # データベース接続情報
    DB_USER: str | None = os.getenv("DB_USER")
    DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")
    DB_HOST: str = "db"
    DB_PORT: str = "5432"
    DB_NAME: str | None = os.getenv("DB_NAME")

    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # CORS 適時追加すること
    ORIGIN_RESOURCES: list[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    # トークン関係
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    API_GATEWAY_STAGE_PATH: str = "/api"
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")

    model_config = SettingsConfigDict(
        case_sensitive=True,
    )


settings = Settings()
