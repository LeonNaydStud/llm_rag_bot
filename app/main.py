from fastapi import FastAPI
from app.api.v1.endpoints import router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
