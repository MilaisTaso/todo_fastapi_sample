from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class Todo(Base):
    __tablename__ = "Todos"

    title: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(Text)
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    def __repr__(self) -> str:
        return (
            "*** TodoOrm ***\n"
            f"id: {self.id!r},\n"
            f"title: {self.title!r},\n"
            f"description: {self.description!r},\n"
            f"completed_at: {self.completed_at!r},\n"
            f"created_at: {self.created_at!r},\n"
            f"updated_at: {self.updated_at!r})"
        )
