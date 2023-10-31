from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status

from src.errors.exception import APIException
from src.errors.messages import ErrorMessage
from src.repository.dependencies import get_repository
from src.repository.crud.user import UserRepository
from src.schemas.requests.user import UserRequest
from src.schemas.response.user import UserResponse

router = APIRouter()

user_repository = Annotated[UserRepository, Depends(get_repository(UserRepository))]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_repo: user_repository, request: UserRequest = Body()):
    user = await user_repo.create(request.model_dump())
    return UserResponse.model_validate(user)
