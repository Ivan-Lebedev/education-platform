from fastapi import APIRouter

from app.infrastructure.config import get_settings

from .content import router as content_router

settings = get_settings()

router = APIRouter(prefix=settings.api.prefix)
router.include_router(content_router)
