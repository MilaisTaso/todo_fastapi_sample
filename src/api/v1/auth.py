import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.lib.auth import authenticate
from src.repository.crud.user import UserRepository
from src.repository.dependencies import get_repository
from src.schemas.response.token import Token

router = APIRouter()

user_repository = Annotated[UserRepository, Depends(get_repository(UserRepository))]

@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login_access_token(
    user_repo: user_repository,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # RequestFormのusernameフィールドをemailように使う
    return await authenticate(
        user_repo,
        form_data.username,
        form_data.password
    )
