from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.users import User
from src.repository.base import DatabaseRepository


class UserRepository(DatabaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    def delete(self, id: UUID):
        pass
