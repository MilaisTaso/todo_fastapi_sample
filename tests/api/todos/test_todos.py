import json
from uuid import UUID
from typing import Dict, Any

import pytest
from httpx import AsyncClient
from fastapi import status

from src.schemas.response.todo import TodoResponse


@pytest.mark.asyncio
class TestTodo:
    url: str = "/api/todo/"
    
    # 現テストケースではcreate, updateで共通仕様が可能
    def assert_req_matches_res(
        self,
        expected_data: Dict[str, Any],
        responce_data: Dict[str, Any] 
    ) -> None:
        for key, value in expected_data.items():
            if key not in responce_data:
                continue
            # assertがFalseの時 ,以降のメッセージを表示できる
            assert responce_data[key] == value, f"Value for '{key}' did not match. Expected: {value}, Found: {responce_data[key]}"
    
    """ get """
    async def test_get_all(self, auth_client: AsyncClient, todo: TodoResponse) -> None:
        # model_damp_json()でpydanticモデルをjson形式で取得
        # json.loads()でpythonが解析できるjsonオブジェクトにする必要がある
        todo_json = json.loads(todo.model_dump_json())

        response = await auth_client.get(self.url)
        
        assert response.status_code == status.HTTP_200_OK
        assert any(todo_json == item for item  in response.json())
        
    
    async def test_get_by_id(self, auth_client: AsyncClient, todo: TodoResponse) -> None:
        todo_id: UUID = todo.id
        response = await auth_client.get(f"{self.url}{todo_id}")

        assert response.status_code == status.HTTP_200_OK
        assert json.loads(todo.model_dump_json()) == response.json()
        
        
    """ create """
    # 下記のようにするとテストケースを作成しやすい
    _create_todo_params = {
        "success": (
            {
                "title": "insert-title-1",
                "description": "insert-description-1",
            },  
            status.HTTP_201_CREATED,
        ),
    }
    
    @pytest.mark.parametrize(
        ("data_in, expected_status"),
        list(_create_todo_params.values()),
        ids=list(_create_todo_params.keys())
    )
    
    async def test_create(
        self,
        auth_client: AsyncClient,
        data_in: Dict[str, Any],
        expected_status: int
    ):
        response = await auth_client.post(self.url, json=data_in)
        create_todo = response.json()
        
        assert response.status_code == expected_status
        assert UUID(create_todo["id"])
        
        self.assert_req_matches_res(
            expected_data=data_in,
            responce_data=create_todo
        )
        


    """ update """
    _update_todo_params = {
        "success": (
            {
                "title": "update-title-1",
                "description": "update-description-1",
                # "completed_at": True ※ pythonのTrueが正しく解釈されず nullになってしまう
            },  
            status.HTTP_200_OK,
        ),
    }

    @pytest.mark.parametrize(
        ("data_in, expected_status"),
        list(_update_todo_params.values()),
        ids=list(_update_todo_params.keys())
    )

    async def test_update(
        self,
        auth_client: AsyncClient,
        todo: TodoResponse,
        data_in: Dict[str, Any],
        expected_status: int
    ):
        response = await auth_client.patch(f"{self.url}{todo.id}", json=data_in)
        
        todo_response = response.json()
        
        assert response.status_code == expected_status
        assert str(todo.id) == todo_response.get("id")
        
        self.assert_req_matches_res(
            expected_data=data_in,
            responce_data=todo_response
        )