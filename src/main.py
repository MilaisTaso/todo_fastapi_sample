from typing import Dict

from fastapi import FastAPI

from src.api.v1.route import router as v1_rooter
from src.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# ルーティング情報をappに追加
app.include_router(v1_rooter, prefix="/api")


@app.get("/")
def root() -> Dict[str, str]:
    return {"detail": "Your Request Successful"}
