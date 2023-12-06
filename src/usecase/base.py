from typing import TypeVar, Generic

from src.repository.base import Repository

UseCase = TypeVar("UseCase", bound="BaseUseCase")

class BaseUseCase(Generic[Repository]):
    pass