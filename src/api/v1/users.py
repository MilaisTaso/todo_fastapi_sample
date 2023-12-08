from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status

from src.errors.exception import APIException
from src.errors.messages import ErrorMessage
from src.database.models.users import User
from src.core.lib.auth import get_current_user
from src.repository.crud.user import UserRepository
from src.repository.dependencies import get_repository
from src.schemas.requests.user import UserRequest
from src.schemas.response.user import UserResponse

router = APIRouter()

user_repository = Annotated[UserRepository, Depends(get_repository(UserRepository))]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_repo: user_repository, body: UserRequest = Body()
) -> UserResponse:
    exists_user: User | None  = user_repo.get_instance(User.email == body.email)
    
    if exists_user:
        raise APIException(ErrorMessage.ALREADY_REGISTED_EMAIL)
    
    user: User = await user_repo.create(body.model_dump())
    return UserResponse.model_validate(user)

@router.patch("{id}", status_code=status.HTTP_200_OK)
async def update_user(
    user: Annotated[User, Depends(get_current_user)],
    user_repo: UserRepository,
    body: UserRequest = Body()
) -> UserResponse:
    ...