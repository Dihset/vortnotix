from fastapi import APIRouter

from src.api.v1.healthcheck.handlers import router as healthcheck_router
from src.api.v1.send.handlers import async_router as send_async_router
from src.api.v1.send.handlers import sync_router as send_sync_router

router = APIRouter(prefix="/v1")
router.include_router(healthcheck_router)
router.include_router(send_async_router)
router.include_router(send_sync_router)
