from typing import Dict

from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI

from src import api
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    openapi_url="/openapi.json",
    debug=settings.DEBUG or False,
)

# 各エンドポイントの追加は各ディレクトリの__init__.pyへ
app.include_router(
    router=api.router,
    prefix="/api",
)

# デバックツールの導入
if settings.DEBUG:
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
    )


@app.get("/", tags=["root"])
def root() -> Dict[str, str]:
    return {"application_name": settings.PROJECT_NAME}
