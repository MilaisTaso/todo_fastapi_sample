from typing import Dict

from fastapi import FastAPI

from src.api.v1.endpoints.todo import router as todo_router
from src.api.v1.endpoints.auth import router as auth_router
from src.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# ルーティング情報をappに追加
app.include_router(todo_router, prefix="/api")
app.include_router(auth_router, prefix="api")


@app.get("/")
def root() -> Dict[str, str]:
    return {"detail": "Your Request Successful"}
