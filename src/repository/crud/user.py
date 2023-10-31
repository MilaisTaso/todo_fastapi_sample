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
from src.schemas.response.token import TokenPayload


class UserRepository(DatabaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)
