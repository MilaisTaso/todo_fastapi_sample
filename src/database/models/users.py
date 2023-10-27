from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class User(Base):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(String(40))
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        index=True,
        nullable=False,
    )
    email_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="0",
    )
    hashed_password: Mapped[str] = mapped_column(Text)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="0")

    def __repr__(self) -> str:
        return (
            f"*** Todo ***"
            f"id: {self.id!r},\n"
            f"full_name: {self.fullname!r},\n"
            f"first_name: {self.first_name!r},\n"
            f"last_name: {self.last_name!r},\n"
            f"email={self.email!r},\n"
            f"email_verified: {self.email_verified!r},\n"
            f"hashed_password: {self.hashed_password!r},\n"
            f"is_admin: {self.is_admin!r},\n"
            f"created_at: {self.created_at!r},\n"
            f"updated_at: {self.updated_at!r})"
        )
