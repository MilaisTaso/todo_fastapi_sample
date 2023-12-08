from uuid import UUID
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.database.models.users import User
from src.database.setting import get_db_session
from src.errors.exception import APIException
from src.errors.messages import ErrorMessage
from src.repository.crud.user import UserRepository
from src.repository.dependencies import get_repository
from src.schemas.response.token import Token, TokenPayload

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_GATEWAY_STAGE_PATH}/auth/login",
    auto_error=False,
)

"""パスワード関係"""


# 渡されたパスワードが同一のものかチェックする
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


# ハッシュ化したパスワードの生成
def hashed_convert(string: str) -> str:
    return bcrypt_context.hash(string)


"""認証関係"""


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta | None = None,
) -> str:
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    # トークンを作る際にidというフィールドも設定できる
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate(
    user_repo: UserRepository, email: str, password: str
) -> Token | None:
    user = await user_repo.get_instance(User.email == email)
    if not user:
        raise APIException(ErrorMessage.FAILURE_LOGIN)

    if not verify_password(password, user.hashed_password):
        return None

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )

    return Token(access_token=access_token)


async def get_current_user(
    security_scopes: SecurityScopes,
    user_repo: Annotated[UserRepository, Depends(get_repository(UserRepository))],
    token: Annotated[str, Depends(oauth2_bearer)],
) -> User:
    """
    クラスメソッドとして実装するとSecurityに依存関係を注入できないため、
    このディレクトリに単体のメソッドとして定義
    """

    if not token:
        raise APIException(ErrorMessage.CouldNotValidateCredentials)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data: TokenPayload = TokenPayload(sub=payload.get("sub"))

    # JWTErrorやValidationErrorは表示しないようfrom Noneとしている
    except (JWTError, ValidationError):
        raise APIException(ErrorMessage.CouldNotValidateCredentials) from None

    user: User | None = await user_repo.get_instance_by_id(token_data.sub)
    if not user:
        raise APIException(ErrorMessage.NOT_FOUND("User"))

    if "admin" in security_scopes.scopes and not user.is_admin:
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error=ErrorMessage.PERMISSION_ERROR,
        )
    return user
