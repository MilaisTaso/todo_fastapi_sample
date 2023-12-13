import logging
import asyncio

from collections.abc import AsyncGenerator
from typing import Any, Dict
from uuid import UUID

import alembic.command
import alembic.config
import pytest
import pytest_asyncio
from pydantic_settings import SettingsConfigDict

from src.core.config import Settings
from src.database.setting import get_db_session
from src.main import app
from fastapi import status
from httpx import AsyncClient
from pytest_postgresql import factories
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# テストレコード作成等に必要
logger.info("root-conftest")


class TestSettings(Settings):
    """Settingsクラスを継承し、テスト用の設定を追加"""
    
    # テスト用ユーザーのパラメータ
    TEST_USER_PARAM: Dict[str, Any] = {
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "hashedPassword": "password",
        "isAdmin": True
    }
    
    model_config = SettingsConfigDict(
        env_file=".env.test"
    )

settings = TestSettings()


# テスト用データベースの作成 権限のあるユーザーでないと作成できない
db_proc = factories.postgresql_noproc(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    dbname=settings.DB_NAME
)
postgresql = factories.postgresql("db_proc")


#alembicを使ってマイグレーションを行う
async def migrate(
    alembic_ini_path: str,
    migrations_path: str,
    url: str,
    connection: Any = None,
    revision: str = "head"
) -> None:
    config = alembic.config.Config(alembic_ini_path)
    config.set_main_option("script_location", migrations_path)
    config.set_main_option("sqlalchemy.url", url)

    # 同期エンジンとコンテキストマネージャーを使用する場合はセッション情報を置きなえる
    if connection:
        config.attributes["connection"] = connection

    # alembic.command.upgrade(config, revision)
    await asyncio.to_thread(alembic.command.upgrade, config, revision)


@pytest_asyncio.fixture
async def engine(postgresql: Any) -> AsyncEngine:
    """engineの作成及びマイグレーションの実行"""

    url: str = settings.DATABASE_URL

    engine = create_async_engine(
        url,
        echo=False,
        poolclass=NullPool
    )
    
    # enginのコネクションを使ってマイグレーション
    async with engine.begin() as conn:
        await migrate(
            alembic_ini_path="alembic.ini",
            migrations_path="migrations",
            url=url,
            connection=conn
        )

    return engine


@pytest_asyncio.fixture
async def db(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    "テストケース用のデータを作成する際に使用するDBセッション"

    TestAsyncScopedSession = async_scoped_session(
        async_sessionmaker(
            engine,
            autocommit=False,
            autoflush=False,
            class_=AsyncSession
            ),
        scopefunc=asyncio.current_task
    )
    
    async with TestAsyncScopedSession() as session:
        yield session
        await session.commit()    

@pytest_asyncio.fixture
async def client(engine: AsyncEngine) -> AsyncClient:
    """HTTP-Clientの作成"""
    
    TestAsyncScopedSession = async_scoped_session(
        async_sessionmaker(
            engine,
            autocommit=False,
            autoflush=False,
            class_=AsyncSession
        ),
        scopefunc=asyncio.current_task
    )

    async def override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
        async with TestAsyncScopedSession() as session:
            yield session
            await session.commit()

    # get_dbをTest用のDBを使用するようにoverrideする
    app.dependency_overrides[get_db_session] = override_get_db_session
    app.debug = False
    return AsyncClient(app=app, base_url=settings.BASE_URL)


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient) -> AsyncClient:
    """AsyncClientに認証ヘッダーを付与する"""
    
    response = await client.post(
        "/api/user/",
        json=settings.TEST_USER_PARAM
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.post(
        "/api/auth/login",
        data={
            "username": settings.TEST_USER_PARAM.get("email"),
            "password": settings.TEST_USER_PARAM.get("hashedPassword"),
        },
    )
    assert response.status_code == status.HTTP_200_OK
    access_token = response.json().get("access_token")
    client.headers = {"authorization": f"Bearer {access_token}"}

    return client


@pytest_asyncio.fixture
async def user_id(auth_client: AsyncClient) -> UUID:
    response = await auth_client.get("/api/user/me")
    
    user_id = response.json().get("id")
    return user_id