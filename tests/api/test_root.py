import pytest

from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
class TestRoot:
    
    async def test_get_root(self, auth_client: AsyncClient):
        response = await auth_client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "todo_fastapi"}