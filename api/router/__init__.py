from fastapi import APIRouter

from .socket.view import router as socket_router

router = APIRouter()
router.include_router(router=socket_router, prefix="/socket")