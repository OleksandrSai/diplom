from fastapi import APIRouter

from .devices.view import router as socket_router

router = APIRouter()
router.include_router(router=socket_router, prefix="/devices")