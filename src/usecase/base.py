from typing import TypeVar, Generic

from src.repository.base import DatabaseRepository

Repository = TypeVar("Repository", bound=DatabaseRepository)

class BaseUseCase(Generic[Repository]):
    pass