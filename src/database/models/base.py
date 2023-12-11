import uuid
from datetime import datetime

from sqlalchemy import DateTime, func, orm
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import current_timestamp


class Base(orm.DeclarativeBase):
    """これを継承してモデルを作成すること"""

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime,
        nullable=False,
        server_default=current_timestamp(),
    )
    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime,
        nullable=False,
        server_default=current_timestamp(),
        onupdate=func.now(),
    )
