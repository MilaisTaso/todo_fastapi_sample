import logging
import os

from collections.abc import AsyncGenerator
from typing import Any, Dict

import alembic.command
import alembic.config
import pytest
import pytest_asyncio
from pydantic_settings import SettingsConfigDict

from src.schemas.requests.user import UserCreateRequest
from src.core.config import Settings
from src.database.setting import get_db_session
from src.main import app
from fastapi import status
from httpx import AsyncClient
from pytest_postgresql import factories
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


pytest.USER_ID = ""

logger.info("root-conftest")


class TestSettings(Settings):
    """Settingsクラスを継承し、テスト用の設定を追加"""
    
    # テスト用ユーザーのパラメータ
    TEST_USER_PARAM: Dict[str, Any] = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "password",
        "is_admin": True
    }

    model_config = SettingsConfigDict(
        env_file=".env.test"
    )


settings = TestSettings()

logger.debug("start: postgres_proc")
db_proc = factories.postgresql_noproc(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER_NAME,
)
postgresql = factories.postgresql("db_proc")
logger.debug("done: postgres_proc")


TEST_USER_CREATE_SCHEMA = UserCreateRequest(**settings.TEST_USER_PARAM)


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
    mysql: Any,
) -> AsyncEngine:
    """fixture: db-engineの作成およびmigrate"""
    logger.debug("fixture:engine")
    # uri = (
    #     f"mysql+aiomysql://{settings.TEST_DB_USER}:"
    #     f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}?charset=utf8mb4"
    # )
    uri = settings.get_database_url(is_async=True)
    # sync_uri = (
    #     f"mysql://{settings.TEST_DB_USER}:"
    #     f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}?charset=utf8mb4"
    # )
    # settings.DATABASE_URI = uri
    engine = create_async_engine(uri, echo=False, poolclass=NullPool)

    # migrate(alembic)はasyncに未対応なため、sync-engineを使用する
    sync_uri = settings.get_database_url()
    print(sync_uri)
    sync_engine = create_engine(sync_uri, echo=False, poolclass=NullPool)
    with sync_engine.begin() as conn:
        migrate(
            migrations_path=settings.MIGRATIONS_DIR_PATH,
            versions_path=os.path.join(settings.MIGRATIONS_DIR_PATH, "versions"),
            alembic_ini_path=os.path.join(settings.ROOT_DIR_PATH, "alembic.ini"),
            connection=conn,
            uri=sync_uri,
        )
        logger.debug("migration end")

    return engine


@pytest_asyncio.fixture
async def db(
    engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """fixture: db-sessionの作成"""
    logger.debug("fixture:db")
    test_session_factory = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
    )

    async with test_session_factory() as session:
        yield session
        await session.commit()


@pytest_asyncio.fixture
async def client(engine: AsyncEngine) -> AsyncClient:
    """fixture: HTTP-Clientの作成"""
    logger.debug("fixture:client")
    test_session_factory = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
    )

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with test_session_factory() as session:
            yield session
            await session.commit()

    # get_dbをTest用のDBを使用するようにoverrideする
    app.dependency_overrides[get_async_db] = override_get_db
    app.debug = False
    return AsyncClient(app=app, base_url="http://test")


@pytest_asyncio.fixture
async def authed_client(client: AsyncClient) -> AsyncClient:
    """fixture: clietnに認証情報をセット"""
    logger.debug("fixture:authed_headers")
    res = await client.post(
        "/users",
        json=TEST_USER_CREATE_SCHEMA.dict(),
    )
    assert res.status_code == status.HTTP_200_OK

    res = await client.post(
        "/auth/login",
        data={
            "username": settings.TEST_USER_EMAIL,
            "password": settings.TEST_USER_PASSWORD,
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


# @pytest.fixture
# def USER_ID(authed_client):
#     return pytest.USER_ID