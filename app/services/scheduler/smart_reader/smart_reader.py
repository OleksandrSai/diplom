from app.utils.orm import UtilsOrm


class SmartReader:
    def __init__(self, controller):
        self.controller = controller
        self.async_orm = UtilsOrm()

    async def raed_all_devices(self):
        for device_id, nwk_address, ieee in await self.async_orm.get_all_devices_adr():
            data = await self.controller.read_device(nwk_address=int(nwk_address),
                                                     ieee=ieee)
            if data:
                await self.async_orm.save_statistic(device_id, nwk_address, data)


