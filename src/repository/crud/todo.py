from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.todos import Todo
from src.repository.base import DatabaseRepository


class TodoRepository(DatabaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Todo, session)