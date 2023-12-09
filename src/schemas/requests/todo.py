from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import ConfigDict, Field, field_serializer

from src.schemas.base import BaseRequestModel


class TodoRequest(BaseRequestModel):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=100)
    completed_at: Optional[bool] = False
    user_id: Optional[UUID] = None

    model_config = ConfigDict(frozen=False)

    @field_serializer("completed_at")
    def insert_complete_datetime(self, is_completed) -> datetime | None:
        if is_completed:
            return datetime.now()
        
        return None
    