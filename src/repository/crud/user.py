from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.users import User
from src.repository.base import DatabaseRepository


class UserRepository(DatabaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def delete(self, id: UUID) -> str:
        return "Delete Successful"
