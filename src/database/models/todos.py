from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base

class Todo(Base):
    __tablename__ = "todos"

    title: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    user = relationship("User", back_populates="todos")

    def __repr__(self) -> str:
        return (
            "*** TodoOrm ***\n"
            f"id: {self.id!r},\n"
            f"title: {self.title!r},\n"
            f"description: {self.description!r},\n"
            f"user_id: {self.user_id}, \n"
            f"completed_at: {self.completed_at!r},\n"
            f"created_at: {self.created_at!r},\n"
            f"updated_at: {self.updated_at!r})"
        )
