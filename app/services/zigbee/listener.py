from zigpy.zcl.clusters.homeautomation import ElectricalMeasurement
from app.utils.orm import UtilsOrm
from zigpy_znp.zigbee.device import ZNPCoordinator
import asyncio
import nest_asyncio


class Listener:

    def __init__(self, application):
        nest_asyncio.apply()
        self.application = application
        self.async_orm = UtilsOrm()
        self.device_initialized_callback = None

    def device_joined(self, device):
        print(f"Device joined: {device}")

    def device_initialized(self, device, *, new=True):
        print(f"new divice  ready {device}")

        if not isinstance(device, ZNPCoordinator):
            try:
                device_type = device.endpoints[1].device_type
                asyncio.run(self.async_orm.add_device(nwk_adr=int(device.nwk),
                                                      ieee=str(device.ieee),
                                                      device_type=device_type))
            except (Exception,):
                pass
