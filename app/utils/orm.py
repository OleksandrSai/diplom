from app.core.async_database import async_session_factory
from app.router.devices import crud
from app.router.statistic import crud as crud_statistic
from app.router.devices.schemas import DevicesDTO, DevicesCreateDTO
from app.router.statistic.schemas import StatisticCreateDTO
from zigpy.profiles.zha import DeviceType
from app.core.models import Device
from sqlalchemy import select
from zigpy.types import EUI64
import redis.asyncio as redis
from app.utils.dependencies import get_redis
import json


class UtilsOrm:

    @staticmethod
    async def get_all_devices() -> list:
        async with async_session_factory as session:
            device: list[Device] = await crud.get_devices(session=session)
            return [DevicesDTO.model_validate(row).model_dump() for row in device]

    @staticmethod
    async def add_device(nwk_adr: int, ieee: str, device_type: DeviceType):
        async with async_session_factory as session:
            query = select(Device).filter_by(nwk_adr=nwk_adr)
            res = await session.execute(query)
            if result := res.scalars().first():
                return DevicesDTO.model_validate(result).model_dump()
            else:
                device_in = DevicesCreateDTO(
                    ieee=ieee,
                    nwk_adr=nwk_adr,
                    type=device_type
                )
                print(session)
                result = await crud.create_device(session, device_in=device_in)
                print(result)
                return DevicesDTO.model_validate(result).model_dump()

    async def get_all_devices_adr(self) -> list[tuple[int, int, str]]:
        return [(device['id'], device['nwk_adr'], device['ieee']) for device in await self.get_all_devices()]

    @staticmethod
    async def save_statistic(device_id: int, nwk_address: int, data):
        redis_conn: redis.Redis = await get_redis()
        data_str = json.dumps(data)
        await redis_conn.set(str(int(nwk_address)), data_str)
        async with async_session_factory as session:
            statistic_in = StatisticCreateDTO(device_id=int(device_id), instant_current=data["current_current"],
                                              instant_voltage=data["current_power"],
                                              total_consumption=data["total_energy"])

            await crud_statistic.create_statistic(session=session, statistic_in=statistic_in)

    @staticmethod
    def ieee_string_to_eui64(ieee_str):
        return EUI64(bytes.fromhex(ieee_str.replace(':', '')))


utils = UtilsOrm()
