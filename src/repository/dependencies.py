from collections.abc import Callable
from typing import Annotated, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.setting import get_db_session
from src.repository.base import Repository

def get_repository(
    repository_cls: Type[Repository],
) -> Callable[[AsyncSession], Repository]:
    """
    Depends()には呼び出し可能オブジェクトしか注入できないので、
    クラスを渡す場合はインスタンスを生成する関数から渡す必要がある
    なお、routing関数でしか使用できないので、注意
    """
    
    def depends_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> Type[Repository]:
        return repository_cls(session)

    return depends_repository
