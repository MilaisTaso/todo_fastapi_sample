import argparse
import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import settings
from src.logger.logger import get_logger
from src.database.models.base import Base


logger = get_logger(__name__)

logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


async def migrate_tables() -> None:
    logger.info("Starting to migrate")

    engine = create_async_engine(settings.DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Done migrating")


async def drop_all_tables() -> None:
    logger.info("start: drop_all_tables")
    """
    全てのテーブルおよび型、Roleなどを削除して、初期状態に戻す(開発環境専用)
    """
    if settings.RUN_ENV != "local":
        # ローカル環境でしか動作させない
        logger.info("drop_all_table() is ENV local only.")
        return

    engine = create_async_engine(settings.DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    logger.info("end: drop_all_tables")


# コマンドから実行する関数が増えそうならpoeとかでタスク定義をしたようがよさそう
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database operations")
    parser.add_argument("command", choices=["migrate", "drop"], help="Command to run")

    args = parser.parse_args()

    if args.command == "migrate":
        asyncio.run(migrate_tables())
    elif args.command == "drop":
        asyncio.run(drop_all_tables())
