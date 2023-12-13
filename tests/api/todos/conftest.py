import datetime
from uuid import UUID

import pytest_asyncio
from src.database.models.todos import Todo
from sqlalchemy.orm import Session


@pytest_asyncio.fixture
async def todo_id(db: Session, user_id: UUID) -> UUID:
    return await insert_todos(db, user_id)


async def insert_todos(db: Session, user_id: UUID) -> UUID:
    now = datetime.datetime.now()
    data = [
        Todo(
            title=f"test-title-{i}",
            description=f"test-description-{i}",
            created_at=now - datetime.timedelta(days=i),
            user_id=user_id
        )
        for i in range(1, 5)
    ]
    db.add_all(data)
    await db.commit()
    
    return data[0].id