from config import settings
from fastapi import FastAPI
import uvicorn
from .router import socket_router
from zigbee.сontroller import Controller
import asyncio

app = FastAPI()
controller = Controller()
app.include_router(router=socket_router, prefix=settings.API_PREFIX)

flag = False


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(controller.start())


@app.get("/")
async def hello_index():
    global flag
    flag = not flag
    if flag:
        await controller.turn_off_device(0x4EE9)
    else:
        await controller.turn_on_device(0x4EE9)
    return {"message": "Device toggled!"}


def start_api():
    uvicorn.run("api.app:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)


