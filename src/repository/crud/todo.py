from uuid import UUID
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.todos import Todo
from src.repository.base import DatabaseRepository


class TodoRepository(DatabaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Todo, session)
    
    async def delete(self, id: UUID) -> None:
        """直接self.model.idとはできない"""
        stmt = (delete(Todo).where(Todo.id == id))
        await self.session.execute(stmt)
        return None