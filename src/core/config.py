from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# pydanticのBaseSettingを使うと環境変数を管谷読み込める
class Settings(BaseSettings):
    """アプリケーションの設定情報"""

    RUN_ENV: str = Field(default="local")
    PROJECT_NAME: str = "todo_fastapi"
    DEBUG: bool = Field(default=False)

    BASE_URL: str = Field(default="http://localhost:8000")

    # データベース接続情報
    DB_USER: str | None = Field(default=None)
    DB_PASSWORD: str | None = Field(default=None)
    DB_HOST: str = Field(default="db")
    DB_PORT: str = Field(default="5432")
    DB_NAME: str | None = Field(default=None)

    @property
    def DATABASE_URL(self) -> str:
        """
        環境編巣を加工して使うときは
        pydanticが環境変数をロードしてからでないとエラーになる
        """

        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"\
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # CORS 適時追加すること
    ORIGIN_RESOURCES: list[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    # トークン関係
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    API_GATEWAY_STAGE_PATH: str = "/api"
    SECRET_KEY: str | None = Field(default=None)

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


# 関数の結果をキャッシュしてくれる 高速な呼び出しが可能に
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
