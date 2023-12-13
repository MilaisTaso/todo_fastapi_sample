from uuid import UUID

import pytest
from httpx import AsyncClient
from fastapi import status

from src.schemas.response.todo import TodoResponse


@pytest.mark.asyncio
class TestTodo:
    url: str = "/api/todo/"
    
    """ get """
    async def test_get_all(self, auth_client: AsyncClient, todo: TodoResponse) -> None:
        response = await auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert any(todo.model_dump()  in response.json())
        
    
    async def test_get_by_id(self, auth_client: AsyncClient, todo: TodoResponse) -> None:
        todo_id: UUID = todo.id
        response = await auth_client.get(f"{self.url}{todo_id}")

        assert response.status_code == status.HTTP_200_OK
        assert str(todo_id) == response.json().get("id")


    """ update """
    @pytest.mark.parametrize(("data", "status", "response"),[
        {
            "title": "update-title",
            "description": "update-description",
            "completedAt": True
        },
        status.HTTP_200_OK,
        
    ])
    async def test_update(self, auth_client: AsyncClient, todo_id: UUID):
        response = await auth_client.patch(f"{self.url}{todo_id}")