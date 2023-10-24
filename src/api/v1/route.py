from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.schemas.todo_request import TodoRequest
from src.database.models.todos import Todos, TodosOrm
from src.database.setting import get_db_session
from src.errors.exception import APIException
from src.errors.messages import ErrorMessage

router = APIRouter(prefix="/v1", tags=["v1"])

session = Annotated[AsyncSession, Depends(get_db_session)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_todos(db: session):
    result = await db.execute(select(TodosOrm))
    todos = result.all()
    return todos


@router.get("/todos/{id}", status_code=status.HTTP_200_OK)
async def get_todo(id: UUID, db: session):
    stmt = select(TodosOrm).where(TodosOrm.id == id)
    result = await db.execute(stmt)
    todo = result.scalar()
    return Todos.model_validate(todo)

@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(db: session, body: TodoRequest = Body()):
    todo = TodosOrm(**body.model_dump())
    db.add(todo)
    await db.flush()
    await db.refresh(todo)

    return Todos.model_validate(todo)

@router.patch("todos/{id}", status_code=status.HTTP_200_OK)
async def update_todo(id: UUID, db:session, body: TodoRequest=Body()):
    todo = await db.scalar(
        select(TodosOrm)
        .where(TodosOrm.id == id)
    )
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)

    stmt = (
        update(TodosOrm).where(TodosOrm.id == id)
        .values(**body.model_dump())
    )
    
    await db.execute(stmt)
    await db.flush()
    await db.refresh(todo)
    return Todos.model_validate(todo)
    

@router.delete("todos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: UUID, db: session):
    stmt = (
        delete(TodosOrm).where(TodosOrm.id == id)
    )
    await db.execute(stmt)
    await db.flush()
    return None
