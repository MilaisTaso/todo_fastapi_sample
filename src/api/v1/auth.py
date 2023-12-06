import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.core.config import settings
from src.core.lib.auth import create_access_token
from src.errors.exception import APIException
from src.errors.messages import ErrorMessage
from src.repository.crud.user import UserRepository
from src.schemas.response.token import Token
from src.usecase.auth import AuthUseCase
from src.usecase.dependencies import get_use_case

router = APIRouter()

auth_use_case = Annotated[AuthUseCase, Depends(get_use_case(AuthUseCase, UserRepository))]


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login_access_token(
    auth_use_case: auth_use_case,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # RequestFormのusernameフィールドをemailように使う
    user = await auth_use_case.authenticate(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise APIException(ErrorMessage.FAILURE_LOGIN)

    access_token_expires = datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)
