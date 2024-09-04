from fastapi import APIRouter

from .scheduler.view import router as scheduler_router
from .devices.view import router as devices_router
from .group.view import router as groups_router
from .ws.view import router as ws_router

router = APIRouter()
router.include_router(router=scheduler_router, prefix="/scheduler")
router.include_router(router=devices_router, prefix="/device")
router.include_router(router=groups_router, prefix="/group")
router.include_router(router=ws_router)
