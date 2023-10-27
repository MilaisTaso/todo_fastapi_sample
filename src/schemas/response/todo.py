from datetime import datetime
from typing import Optional

from src.schemas.base import BaseResponseModel


class TodoResponse(BaseResponseModel):
    title: str
    description: str
    completed_at: Optional[datetime] = None
