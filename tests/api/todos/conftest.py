import datetime
from typing import List
from uuid import UUID

import pytest_asyncio
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from src.database.models.todos import Todo
from src.schemas.response.todo import TodoResponse


@pytest_asyncio.fixture
async def todos(db: Session, user_id: UUID) -> List[TodoResponse]:
    now = datetime.datetime.now()
    todo_data = [
        {
            "title": f"test-title-{i}",
            "description": f"test-description-{i}",
            "created_at": now - datetime.timedelta(days=i),
            "user_id": user_id
        } for i in range(1, 5)
    ]

    # Insert文を実行
    await db.execute(insert(Todo), todo_data)
    await db.commit()

    # insesrt...returningを使用したがうまくいかなかった
    result = await db.execute(select(Todo))
    todos = result.scalars().all()

    return [TodoResponse.model_validate(todo) for todo in todos]


@pytest_asyncio.fixture
async def todo_id(todos: List[TodoResponse]) -> UUID:

    return todos[0].id