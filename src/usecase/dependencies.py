from collections.abc import Callable
from typing import Annotated, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.setting import get_db_session
from src.repository.base import Repository
from src.usecase.base import UseCase


def get_use_case(
    use_case_cls: Type[UseCase],
    repository_cls: Repository,
) -> Callable[[AsyncSession], UseCase]:
    """
    UseCase内で使用するRepositoryが一つならこちらで対応
    複数なら個別に呼び出し関数を作成する
    """
    
    def depends_use_case(session: Annotated[AsyncSession, Depends(get_db_session)]) -> Type[UseCase]:
        repository = repository_cls(session)
        return use_case_cls(repository)

    return depends_use_case