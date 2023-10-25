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

@router.get("/auth")
async def get_user():
    return {"user": "authenticated"}