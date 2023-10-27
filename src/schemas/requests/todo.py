from pydantic import Field

from src.schemas.base import BaseRequestModel


class TodoRequest(BaseRequestModel):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=100)
