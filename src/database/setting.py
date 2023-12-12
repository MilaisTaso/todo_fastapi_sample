from asyncio import current_task
from collections.abc import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import settings


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
    )
    """
    async_scoped_sessionはスレッドローカルではない
    そのため、scope_func（コールバック）にセッションのIDを返すことで、
    どのスレッド（スコープ）で実行するか指定する必要がある
    current_task()はasyncioの機能で現在のタスク自身のIDを返す
    それによりスレッドローカルと同じ接続ができるようになる
    """

    AsyncScopedSession = async_scoped_session(
        async_sessionmaker(
            engine,
            autocommit=False,
            autoflush=False,
        ),
        scopefunc=current_task
    )

    async with AsyncScopedSession() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()
