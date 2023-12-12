from datetime import datetime
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.users import User
from src.repository.base import DatabaseRepository


class UserRepository(DatabaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def soft_delete(self, instance: User) -> User:
        instance.deleted_at = datetime.now()

        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)

        return instance
