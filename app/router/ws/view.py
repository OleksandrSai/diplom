from fastapi import APIRouter, Depends
from fastapi import WebSocket
import redis.asyncio as redis
from aioredis import Redis
import json

router = APIRouter(tags=["ws"])
active_connections: list[WebSocket] = []


async def get_redis() -> Redis:
    return await Redis.from_url("redis://localhost")


@router.get("/")
async def read_root(redis_conn: redis.Redis = Depends(get_redis)):
    await redis_conn.set("my_key", "Hello, Redis!")
    value = await redis_conn.get("my_key")
    return {"message": value.decode("utf-8")}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, redis_conn: redis.Redis = Depends(get_redis)):
    await connect_websocket(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            devices = json.loads(data)
            nwk_address = [key["nwk_adr"] for key in devices]
            polling_data = []
            for address in nwk_address:
                res_redis = await redis_conn.get(str(address))
                if res_redis:
                    polling_data.append({"nwk_adr": address} | json.loads(res_redis.decode()))
            result = json.dumps(polling_data)
            await websocket.send_text(result)
    except Exception as exc:
        print(exc)
        await disconnect_websocket(websocket)


async def connect_websocket(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)


async def disconnect_websocket(websocket: WebSocket):
    active_connections.remove(websocket)


async def get_values_from_redis(keys, redis_conn: redis.Redis = Depends(get_redis)):
    return await redis_conn.mget(keys)

