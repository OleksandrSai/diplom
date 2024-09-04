from app.utils.orm import UtilsOrm
from app.router.ws.view import get_redis
from aioredis import Redis
import json
from zigpy.types import EUI64


class SmartReader:
    def __init__(self, controller):
        self.controller = controller
        self.async_orm = UtilsOrm()

    async def raed_all_devices(self):
        for nwk_address, ieee in await self.async_orm.get_all_devices_adr():
            data = await self.controller.read_device(nwk_address=int(nwk_address),
                                                     ieee=self.async_orm.ieee_string_to_eui64(ieee))

            data_str = json.dumps(data)
            redis = await get_redis()
            await redis.set(str(int(nwk_address)), data_str)
