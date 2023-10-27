from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.todos import Todo
from src.database.setting import get_db_session
from src.errors.exception import APIException
from src.errors.messages import ErrorMessage
from src.schemas.requests.todo import TodoRequest
from src.schemas.response.todo import TodoResponse

router = APIRouter()

session = Annotated[AsyncSession, Depends(get_db_session)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_todos(db: session):
    result = await db.execute(select(Todo))
    return [TodoResponse(todo) for todo in result.all()]


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_todo(id: UUID, db: session):
    stmt = select(Todo).where(Todo.id == id)
    result = await db.execute(stmt)
    todo = result.scalar()
    return TodoResponse.model_validate(todo)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(db: session, body: TodoRequest = Body()):
    todo = Todo(**body.model_dump())
    db.add(todo)
    await db.flush()
    await db.refresh(todo)

    return TodoResponse.model_validate(todo)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_todo(id: UUID, db: session, body: TodoRequest = Body()):
    todo = await db.scalar(select(Todo).where(Todo.id == id))
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)

    stmt = update(Todo).where(Todo.id == id).values(**body.model_dump())

    await db.execute(stmt)
    await db.flush()
    await db.refresh(todo)
    return TodoResponse.model_validate(todo)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: UUID, db: session):
    stmt = delete(Todo).where(Todo.id == id)
    await db.execute(stmt)
    await db.flush()
    return None
