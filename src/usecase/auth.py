from typing import Annotated, Optional

from fastapi import Depends, status
from fastapi.security import SecurityScopes
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.lib.auth import oauth2_bearer, token_decoded, verify_password
from src.database.models.users import User
from src.errors.exception import APIException
from src.errors.messages import ErrorMessage
from src.repository.base import DatabaseRepository
from src.repository.crud.user import UserRepository
from src.schemas.response.token import TokenPayload
from src.usecase.base import BaseUseCase
from src.repository.dependencies import get_repository

class AuthUseCase(BaseUseCase):
    def __init__(self) -> None:
        self.user_repo = Annotated[UserRepository, Depends(get_repository(UserRepository))]

    async def authenticate(self, email: str, password: str) -> User | None:
        user = await self.user_repo.get_instance(User.email == email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    # ルーティングに直接渡すのでこの関数内で例外を発生させなければならない
    # 処理が多いのでUseCaseを採用した方が良かった
    async def get_current_user(
        self,
        token: Annotated[str,Depends(oauth2_bearer)],
    ) -> User:
        if not token:
            raise APIException(ErrorMessage.CouldNotValidateCredentials)

        try:
            payload = token_decoded(token)
            print(payload)
            token_data = TokenPayload(sub=payload.get("sub"))
        #JWTErrorやValidationErrorは表示しないようfrom Noneとしている
        except (JWTError, ValidationError):
            raise APIException(ErrorMessage.CouldNotValidateCredentials) from None

        user = await self.user_repo.get_instance_by_id(token_data)
        if not user:
            raise APIException(ErrorMessage.NOT_FOUND("User"))

        return user