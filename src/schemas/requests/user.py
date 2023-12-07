from typing import Any, Optional

from pydantic import ConfigDict, EmailStr, Field, field_serializer

from src.core.lib.auth import hashed_convert
from src.schemas.base import BaseRequestModel


class UserRequest(BaseRequestModel):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if not self.full_name:
            self.full_name = f"{self.first_name} {self.last_name}"

    first_name: str = Field(min_length=1, max_length=20)
    last_name: str = Field(min_length=1, max_length=20)
    full_name: Optional[str] = None
    email: EmailStr
    hashed_password: str = Field(min_length=8, max_length=20)  # ハッシュにする前のパスワード
    is_admin: bool = Field(default=False)

    model_config = ConfigDict(
        frozen=False,  # __init__で値を生成するため
    )

    # dictへ変換する際にパスワードをハッシュ化する
    @field_serializer("hashed_password")
    def get_hashed_password(self, password: str) -> str:
        return hashed_convert(password)
