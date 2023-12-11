import logging
from typing import Dict

from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import api
from src.core.config import settings
from src.logger.logger import get_logger

# loggerの設定
logger = get_logger(__name__)

# pythonのlogging.filterを継承したクラス
# swigger(/docs)自体のログを非表示にする

class NoParsingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return not record.getMessage().find("/docs") >= 0

# uvicornのログに対して上記を適応
logging.getLogger("uvicorn.access").addFilter(NoParsingFilter())


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    openapi_url="/openapi.json",
    debug=settings.DEBUG or False,
)

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins= settings.ORIGIN_RESOURCES,
    #正規表現使用例
    #allow_origin_regex=r"^https?:\/\/([\w\-\_]{1,}\.|)example\.com",
    allow_methods=["*"],
    allow_headers=["*"],
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
