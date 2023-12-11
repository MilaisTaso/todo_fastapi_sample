from datetime import datetime
from typing import Optional

from pydantic import EmailStr

from src.schemas.base import BaseResponseModel


class UserResponse(BaseResponseModel):
    full_name: str
    first_name: str
    last_name: str
    email: EmailStr
    email_verified: bool
    hashed_password: str
    is_admin: bool
    deleted_at: Optional[datetime] = None
