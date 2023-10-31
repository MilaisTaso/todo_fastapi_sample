from collections.abc import Callable
from typing import Annotated, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.setting import get_db_session
from src.repository.base import Base, DatabaseRepository

Repository = TypeVar("Repository", bound=DatabaseRepository)


def get_repository(
    repository: type[Repository],
) -> Callable[[AsyncSession], type[Repository]]:
    """
    Depends()には呼び出し可能オブジェクトしか注入できないので、
    クラスを渡す場合はインスタンスを生成する関数から渡す必要がある
    なお、routing関数でしか使用できないので、注意
    """

    def func(session: Annotated[AsyncSession, Depends(get_db_session)]):
        return repository(session)

    return func
