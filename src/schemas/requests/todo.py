from typing import Optional
from uuid import UUID

from pydantic import ConfigDict, Field

from src.schemas.base import BaseRequestModel


class TodoRequest(BaseRequestModel):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=100)

    model_config = ConfigDict(frozen=False)
