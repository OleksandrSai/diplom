from __future__ import annotations
from config import settings
from fastapi import FastAPI
import uvicorn
from .router import router as united_router
from .services.zigbee.сontroller import Controller
from .services.scheduler.scheduler import Scheduler
import asyncio
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
controller = Controller()
scheduler = Scheduler(controller)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=united_router, prefix=settings.API_PREFIX)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(controller.start())
    asyncio.create_task(scheduler.start())


@app.on_event("shutdown")
async def startup_event():
    await controller.stop()


def start_api():
    uvicorn.run("app.app:app", host=settings.API_HOST, port=settings.API_PORT, reload=False)


