import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings

# 作成したいテーブル定義もインポートする必要あり
from src.database.models import todos
from src.database.models.base import Base

logging.basicConfig()
logger = logging.getLogger()

logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


async def migrate_tables() -> None:
    logger.info("Starting to migrate")

    engine = create_async_engine(settings.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Done migrating")


if __name__ == "__main__":
    asyncio.run(migrate_tables())
