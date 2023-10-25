from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from sqlalchemy import DateTime, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class UsersOrm(Base):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(String(40))
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(
        String(200), unique=True, index=True, nullable=False,
    )
    email_verified: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="0",
    )
    hashed_password: Mapped[str] = mapped_column(Text)
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="0"
    )

    def __repr__(self) -> str:
        return (
            f"UsersOrm("
            f"id={self.id!r},"
            f"full_name={self.fullname!r},"
            f"first_name={self.first_name!r},"
            f"last_name={self.last_name!r},"
            f"email={self.email!r},"
            f"email_verified={self.email_verified!r},"
            f"hashed_password={self.hashed_password!r},"
            f"is_admin={self.is_admin!r},"
            f"created_at={self.created_at!r},"
            f"updated_at={self.updated_at!r})"
        )


class Todos(BaseModel):
    id: UUID
    title: str
    description: str
    complated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
