from uuid import UUID

import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
class TestTodo:
    url: str = "/api/todo/"
    
    async def test_get_all(self, auth_client: AsyncClient, todo_id: UUID):
        response = await auth_client.get(self.url)
        
        print(f"todo_id:{todo_id}")
        
        data_list = response.json()
        
        print(data_list)

        assert response.status_code == status.HTTP_200_OK
        assert any(str(todo_id) == data["id"] for data in data_list)