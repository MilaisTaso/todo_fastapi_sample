from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.users import User
from src.database.setting import get_db_session
from src.errors.exception import APIException
from src.errors.messages import ErrorMessage
from src.schemas.requests.user import UserRequest
from src.schemas.response.user import UserResponse

router = APIRouter()

session = Annotated[AsyncSession, Depends(get_db_session)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: session, request: UserRequest = Body()):
    user: User = User(**request.model_dump())
    await db.add(user)
    await db.flush()
    await db.refresh()

    return UserResponse.model_validate(user)
