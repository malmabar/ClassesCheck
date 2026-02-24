from fastapi import APIRouter

from app.api.routes.checks import router as checks_router
from app.api.routes.health import router as health_router
from app.api.routes.imports import router as import_router
from app.api.routes.pipeline import router as pipeline_router
from app.api.routes.runs import router as runs_router


api_router = APIRouter()
api_router.include_router(checks_router)
api_router.include_router(health_router)
api_router.include_router(import_router)
api_router.include_router(pipeline_router)
api_router.include_router(runs_router)
