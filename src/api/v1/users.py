from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, status, Security

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
    exists_user: User | None  = await user_repo.get_instance(User.email == body.email)
    
    if exists_user:
        raise APIException(ErrorMessage.ALREADY_REGISTED_EMAIL)
    
    user: User = await user_repo.create(body.model_dump())
    return UserResponse.model_validate(user)

@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_user(
    id: UUID,
    user_repo: user_repository,
    currnet_user: Annotated[User, Security(get_current_user)],
    body: UserRequest = Body()
):
    exists_user: User | None = await user_repo.get_instance_by_id(id)
    
    if not exists_user:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    
    if exists_user.id != currnet_user.id or not currnet_user.is_admin:
        raise APIException(ErrorMessage.PERMISSION_ERROR("編集"))
    
    user: User = await user_repo.update(exists_user, body.model_dump())
    
    return UserResponse.model_validate(user)