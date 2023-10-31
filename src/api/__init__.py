"""apiルーティング"""

from fastapi import APIRouter

from src.api.v1 import auth, todos, users

router = APIRouter()

router.include_router(router=todos.router, prefix="/todo", tags=["todo"])

router.include_router(router=users.router, prefix="/user", tags=["user"])

router.include_router(router=auth.router, prefix="/auth", tags=["auth"])
