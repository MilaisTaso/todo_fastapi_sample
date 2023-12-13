from typing import Any

import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
class TestTodo:
    url: str = "/todo"
    
    # @pytest.mark.parametrize()