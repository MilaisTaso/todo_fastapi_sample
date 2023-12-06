from typing import Annotated

from fastapi import Depends, status
from fastapi.security import SecurityScopes
from jose.exceptions import JWTError
from pydantic import ValidationError

from src.core.lib.auth import oauth2_bearer, token_decoded, verify_password
from src.database.models.users import User
from src.errors.exception import APIException
from src.errors.messages import ErrorMessage
from src.repository.crud.user import UserRepository
from src.schemas.response.token import TokenPayload
from src.usecase.base import BaseUseCase


class AuthUseCase(BaseUseCase):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repo = user_repository

    async def authenticate(self, email: str, password: str) -> User | None:
        user = await self.user_repo.get_instance(User.email == email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def get_current_user(
        self,
        security_scopes: SecurityScopes,
        token: Annotated[str,Depends(oauth2_bearer)],
    ) -> User:
        if not token:
            raise APIException(ErrorMessage.CouldNotValidateCredentials)

        try:
            payload = token_decoded(token)
            token_data = TokenPayload(sub=payload.get("sub"))

        #JWTErrorやValidationErrorは表示しないようfrom Noneとしている
        except (JWTError, ValidationError):
            raise APIException(ErrorMessage.CouldNotValidateCredentials) from None

        user: User = await self.user_repo.get_instance_by_id(token_data)
        if not user:
            raise APIException(ErrorMessage.NOT_FOUND("User"))
        
        if "admin" in security_scopes.scopes and not user.is_admin:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                error=ErrorMessage.PERMISSION_ERROR,
            )
        return user