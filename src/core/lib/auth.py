from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.errors.exception import APIException
from src.errors.messages import ErrorMessage

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


def token_decoded(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as err:
        raise err
