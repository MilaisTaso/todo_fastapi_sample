import logging
import os
from asyncio import current_task

from collections.abc import AsyncGenerator
from typing import Any, Dict

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

settings = TestSettings()

logger.debug("start: postgres_proc")

# テスト用データベースの作成 権限のあるユーザーでないと作成できない
db_proc = factories.postgresql_noproc(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
)
postgresql = factories.postgresql("db_proc")

logger.debug("done: postgres_proc")


#alembicを使ってマイグレーションを行う
def migrate(
    versions_path: str,
    migrations_path: str,
    uri: str,
    alembic_ini_path: str,
    connection: Any = None,
    revision: str = "head",
) -> None:
    config = alembic.config.Config(alembic_ini_path)
    config.set_main_option("version_locations", versions_path)
    config.set_main_option("script_location", migrations_path)
    config.set_main_option("sqlalchemy.url", uri)

    if connection:
        config.attributes["connection"] = connection

    alembic.command.upgrade(config, revision)


@pytest_asyncio.fixture
async def engine(
    postgresql: Any,
) -> AsyncEngine:
    """engineの作成及びマイグレーションの実行"""
    logger.debug("start: create engine")
    url: str = settings.DATABASE_URL

    engine = create_async_engine(
        url,
        echo=False,
        poolclass=NullPool
    )

    migrate(
        migrations_path=settings.MIGRATIONS_DIR_PATH,
        versions_path=os.path.join(settings.MIGRATIONS_DIR_PATH, "versions"),
        alembic_ini_path=os.path.join(settings.ROOT_DIR_PATH, "alembic.ini"),
        uri=url,
    )
    logger.debug("done: migrations")

    return engine


@pytest_asyncio.fixture
async def client(engine: AsyncEngine) -> AsyncClient:
    """HTTP-Clientの作成"""
    logger.debug("start:create AsyncClient")
    
    TestAsyncScopedSession = async_scoped_session(
        async_sessionmaker(
            engine,
            autocommit=False,
            autoflush=False,
        ),
        scopefunc=current_task
    )

    async def override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
        async with TestAsyncScopedSession() as session:
            yield session
            await session.commit()

    # get_dbをTest用のDBを使用するようにoverrideする
    app.dependency_overrides[get_db_session] = override_get_db_session
    app.debug = False
    return AsyncClient(app=app, base_url="http://test")


@pytest_asyncio.fixture
async def authed_client(client: AsyncClient) -> AsyncClient:
    """fixture: clietnに認証情報をセット"""
    logger.debug("fixture:authed_headers")
    res = await client.post(
        "/users",
        json=settings.TEST_USER_PARAM,
    )
    assert res.status_code == status.HTTP_200_OK

    res = await client.post(
        "/auth/login",
        data={
            "username": settings.TEST_USER_PARAM.get("email"),
            "password": settings.TEST_USER_PARAM.get("hashed_password"),
        },
    )
    assert res.status_code == status.HTTP_200_OK
    access_token = res.json().get("access_token")
    client.headers = {"authorization": f"Bearer {access_token}"}

    # テスト全体で使用するので、グローバル変数とする
    res = await client.get("users/me")
    assert res.json().get("id")
    pytest.USER_ID = res.json().get("id")

    return client
