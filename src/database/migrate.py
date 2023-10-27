import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import settings
from src.database.models.base import Base
from src.database.models.todos import Todo

# 作成したいテーブル定義もインポートする必要あり 呼び出すテーブルの順番は重要
from src.database.models.users import User

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
