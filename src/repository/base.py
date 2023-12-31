from typing import Any, Dict, Generic, TypeVar
from uuid import UUID

from sqlalchemy import BinaryExpression, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.base import Base

Model = TypeVar("Model", bound=Base)


class DatabaseRepository(Generic[Model]):
    """Repository for performing database queries."""

    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def create(self, data: Dict[str, Any]) -> Model:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: Model, data: Dict[str, Any]) -> Model:
        for key, value in data.items():
            # valueがNoneでも更新するので注意
            if not hasattr(instance, key):
                continue
            setattr(instance, key, value)

        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def get_instance_by_id(self, id: UUID) -> Model | None:
        # get()は主キーに基づいたインスタンスを返す
        return await self.session.get(self.model, id)

    async def get_instance(self, *expressions: BinaryExpression) -> Model | None:
        if not expressions:
            return None
        stmt = select(self.model).where(*expressions)
        return await self.session.scalar(stmt)

    async def get_instance_list(
        self,
        *expressions: BinaryExpression,
    ) -> list[Model]:
        query = select(self.model)
        if expressions:
            query = query.where(*expressions)
        return list(await self.session.scalars(query))
