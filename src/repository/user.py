from fastapi import Depends, status
from fastapi.security import SecurityScopes
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.lib.auth import reusable_oauth2, token_decoded, verify_password
from src.database.models.users import User
from src.errors.exception import APIException
from src.errors.messages import ErrorMessage
from src.repository.base import DatabaseRepository
from src.schemas.response.token import TokenPayload


class UserRepository(DatabaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def authenticate(self, email: str, password: str) -> User | None:
        user = await super().get_instance(User.email == email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    # ルーティングに直接渡すのでこの関数内で例外を発生させなければならない
    # 処理が多いのでUseCaseを採用した方が良かった
    async def get_current_user(
        security_scopes: SecurityScopes,
        token: str = Depends(reusable_oauth2),
    ) -> User:
        if not token:
            raise APIException(ErrorMessage.CouldNotValidateCredentials)

        try:
            payload = token_decoded(token)
            token_data = TokenPayload.model_validate(payload)
        except (JWTError, ValidationError):
            raise APIException(ErrorMessage.CouldNotValidateCredentials) from None
        user = await super().get_instance_by_id(token_data.sub)
        if not user:
            raise APIException(ErrorMessage.NOT_FOUND("User"))

        # SecurityScopesにはlist[str]しか渡せないので利用する場合はデータベースのカラムの工夫も必要
        if "is_admin=True" in security_scopes.scopes and not user.is_admin:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                error=ErrorMessage.PERMISSION_ERROR,
            )
        return user
