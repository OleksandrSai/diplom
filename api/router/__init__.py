from fastapi import APIRouter

from .scheduler.view import router as scheduler_router

router = APIRouter()
router.include_router(router=scheduler_router, prefix="/scheduler")
