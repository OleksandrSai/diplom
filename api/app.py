from config import settings
from fastapi import FastAPI, WebSocket
import uvicorn
from .router import router as scheduler_router
from zigbee.сontroller import Controller
import asyncio
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
controller = Controller()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=scheduler_router, prefix=settings.API_PREFIX)

flag = False
active_connections: list[WebSocket] = []


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(controller.start())


@app.on_event("shutdown")
async def startup_event():
    await controller.stop()


@app.get("/li")
async def hello_index1():
    while True:
        await asyncio.sleep(15)
        res = await controller.read_interval()
        await broadcast_message(res)


async def connect_websocket(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)


async def disconnect_websocket(websocket: WebSocket):
    active_connections.remove(websocket)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connect_websocket(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            await websocket.send_text(f"Message received: {data}")
    except Exception:
        await disconnect_websocket(websocket)


async def broadcast_message(message: str):
    for connection in active_connections:
        await connection.send_text(message)


@app.get("/")
async def hello_index():
    global flag
    flag = not flag
    try:
        if flag:
            await controller.turn_off_device(0x4EE9)
        else:
            await controller.turn_on_device(0x4EE9)
    except Exception as e:
        print(e)
    return {"message": "Device toggled!"}


def start_api():
    uvicorn.run("api.app:app", host=settings.API_HOST, port=settings.API_PORT, reload=False)


