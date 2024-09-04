from app.core.async_database import async_session_factory
from app.router.devices import crud
from app.router.devices.schemas import DevicesDTO, DevicesCreateDTO
from app.core.models import Device
from sqlalchemy import select
from zigpy.types import EUI64

class UtilsOrm:

    @staticmethod
    async def get_all_devices() -> list:
        async with async_session_factory as session:
            device: list[Device] = await crud.get_devices(session=session)
            return [DevicesDTO.model_validate(row).model_dump() for row in device]

    @staticmethod
    async def add_device(nwk_adr: int, ieee: str):
        async with async_session_factory as session:
            query = select(Device).filter_by(nwk_adr=nwk_adr)
            res = await session.execute(query)
            if result := res.scalars().first():
                return DevicesDTO.model_validate(result).model_dump()
            else:
                device_in = DevicesCreateDTO(
                    ieee=ieee,
                    nwk_adr=nwk_adr
                )
                result = await crud.create_device(session, device_in=device_in)
                return DevicesDTO.model_validate(result).model_dump()

    async def get_all_devices_adr(self) -> list[tuple[int, str]]:
        return [(device['nwk_adr'], device['ieee']) for device in await self.get_all_devices()]

    @staticmethod
    def ieee_string_to_eui64(ieee_str):
        return EUI64(bytes.fromhex(ieee_str.replace(':', '')))
