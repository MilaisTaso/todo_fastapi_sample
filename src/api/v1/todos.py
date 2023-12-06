from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, status, Security

from src.errors.exception import APIException
from src.errors.messages import ErrorMessage
from src.schemas.requests.todo import TodoRequest
from src.schemas.response.todo import TodoResponse
from src.repository.dependencies import get_repository
from src.repository.crud.todo import TodoRepository
from src.repository.crud.user import UserRepository
from src.usecase.auth import AuthUseCase
from src.usecase.dependencies import get_use_case

router = APIRouter()

todo_repository = Annotated[TodoRepository, Depends(get_repository(TodoRepository))]
auth_use_case = Annotated[AuthUseCase, Depends(get_use_case(AuthUseCase, UserRepository))]

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(auth_use_case.get_current_user, scopes=[])]
    )
async def create_todo(
    todo_repo: todo_repository,
    body: TodoRequest = Body()
) -> TodoResponse:
    todo = todo_repo.create(body.model_dump())

    return TodoResponse.model_validate(todo)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_todos(todo_repo: todo_repository):
    todos = await todo_repo.get_instance_list()
    return todos


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_todo(id: UUID, todo_repo: todo_repository):
    todo = todo_repo.get_instance_by_id(id)
    return TodoResponse.model_validate(todo)

@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_todo(id: UUID, todo_repo: todo_repository, body: TodoRequest = Body()):
    todo = await todo_repo.get_instance_by_id(id)
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)

    update_todo = todo_repo.update(todo, body.model_dump())
    return TodoResponse.model_validate(update_todo)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: UUID, todo_repo: todo_repository):
    todo = await todo_repo.get_instance_by_id(id)
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    
    todo_repo.delete(id)
    return None
