from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import ConfigDict, Field, field_serializer

from src.schemas.base import BaseRequestModel


class TodoRequest(BaseRequestModel):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=100)

    model_config = ConfigDict(frozen=False)


class TodoCreateRequest(TodoRequest):
    user_id: Optional[UUID] = None


class TodoUpdateRequest(TodoRequest):
    completed_at: bool = Field(default=False)

    # データベースのカラムはDatetime型なのでmodel_validate()で必ず変換すること
    @field_serializer("completed_at")
    def insert_complete_datetime(self, is_completed) -> datetime | None:
        if is_completed:
            return datetime.now()

        return None
