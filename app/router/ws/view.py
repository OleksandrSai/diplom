from fastapi import APIRouter, Depends
from fastapi import WebSocket
import redis.asyncio as redis
import json
from app.utils.dependencies import get_redis

router = APIRouter(tags=["ws"])
active_connections: list[WebSocket] = []


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
                if res_redis.decode() is not None:
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


