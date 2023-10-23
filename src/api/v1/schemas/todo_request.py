from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.database.models.base import Base


class TodoRequest(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=100)
