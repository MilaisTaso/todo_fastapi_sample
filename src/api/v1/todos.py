from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Security, status

from src.core.lib.auth import get_current_user
from src.database.models.todos import Todo
from src.database.models.users import User
from src.errors.exception import APIException
from src.errors.messages import ErrorMessage
from src.repository.crud.todo import TodoRepository
from src.repository.dependencies import get_repository
from src.schemas.requests.todo import TodoRequest
from src.schemas.response.todo import TodoResponse
from src.schemas.response.message import MessageResponse

router = APIRouter()

todo_repository = Annotated[TodoRepository, Depends(get_repository(TodoRepository))]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_todo(
    todo_repo: todo_repository,
    user: Annotated[User, Security(get_current_user)],
    body: TodoRequest = Body(),
) -> TodoResponse:
    body.user_id = user.id
    todo: Todo = await todo_repo.create(body.model_dump())

    return TodoResponse.model_validate(todo)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_todos(todo_repo: todo_repository) -> List[TodoResponse]:
    todos: List[Todo] = await todo_repo.get_instance_list()
    return [TodoResponse.model_validate(todo) for todo in todos]


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_todo(id: UUID, todo_repo: todo_repository) -> TodoResponse:
    todo = todo_repo.get_instance_by_id(id)
    return TodoResponse.model_validate(todo)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_todo(
    id: UUID, todo_repo: todo_repository, body: TodoRequest = Body()
) -> TodoResponse:
    todo = await todo_repo.get_instance_by_id(id)
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)

    update_todo = todo_repo.update(todo, body.model_dump())
    return TodoResponse.model_validate(update_todo)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: UUID, todo_repo: todo_repository) -> str:
    todo = await todo_repo.get_instance_by_id(id)
    if not todo:
        raise APIException(ErrorMessage.ID_NOT_FOUND)

    result = todo_repo.delete(id)
    return MessageResponse(message=result)
