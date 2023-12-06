from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, status, Security

from src.core.lib.auth import get_current_user
from src.errors.exception import APIException
from src.errors.messages import ErrorMessage
from src.schemas.requests.todo import TodoRequest
from src.schemas.response.todo import TodoResponse
from src.database.models.users import User
from src.repository.dependencies import get_repository
from src.repository.crud.todo import TodoRepository

router = APIRouter()

todo_repository = Annotated[TodoRepository, Depends(get_repository(TodoRepository))]

@router.post("/", status_code=status.HTTP_201_CREATED,)
async def create_todo(
    todo_repo: todo_repository,
    user: Annotated[User, Security(get_current_user)],
    body: TodoRequest = Body()
) -> TodoResponse:
    body.user_id = user.id
    todo = await todo_repo.create(body.model_dump())

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
