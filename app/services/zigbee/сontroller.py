import asyncio
from zigpy_znp.zigbee.application import ControllerApplication
from config import settings
from .listener import Listener
import async_timeout
from zigpy import types as t
from zigpy.types import EUI64
from app.utils.orm import UtilsOrm
from app.utils.dependencies import get_redis
import json
from app.utils.orm import utils
from zigpy.device import Device
import nest_asyncio

nest_asyncio.apply()


class Controller:
    def __init__(self):
        self.app = None
        self.pan_id = settings.ZIGBEE_PAN_ID
        self.chanel = settings.ZIGBEE_CHANEL
        self.serial_port = settings.ZIGBEE_SERIAL_PORT
        self.key = settings.ZIGBEE_KEY
        self.configurate_controller()
        self.shutdown_event = None
        self.listener = None
        self.async_orm = UtilsOrm()

    # async def discover_attributes(self, device, endpoint_id, cluster_id):
    #     cluster = device.endpoints[endpoint_id].clusters[cluster_id]
    #     attributes = await cluster.discover_attributes()
    #     return attributes

    async def read_attributes(self, cluster, attribute_ids) -> dict:
        try:
            async with async_timeout.timeout(10):
                result = await cluster.read_attributes(attribute_ids)
                return result[0]
        except asyncio.TimeoutError:
            print(f"Timeout while reading attributes {attribute_ids} from cluster {cluster.cluster_id}")
            return {}
        except Exception as e:
            print(f"Error reading attributes {attribute_ids} from cluster {cluster.cluster_id}: {e}")
            return {}

    async def read_device(self, nwk_address: int, ieee: str) -> dict:
        try:
            ieee = EUI64.convert(ieee)
            device = self.app.get_device(nwk=nwk_address, ieee=ieee)
            attribute_ids = [0x0000]
            endpoint = device.endpoints[1]

            attr_dict, _ = await endpoint.smartenergy_metering.read_attributes(attribute_ids)
            total_energy = attr_dict.get(0x0000)

            attribute_ids = [0x0505, 0x0508, 0x050B]
            attr_dict, _ = await endpoint.electrical_measurement.read_attributes(attribute_ids)
            current_power = attr_dict.get(0x050B, 0)
            current_current = attr_dict.get(0x0508, 0) / 100
            attribute_ids = [0x0000]
            attr_dict, _ = await endpoint.on_off.read_attributes(attribute_ids)
            current_state = attr_dict.get(0x0000)

            return {
                "current_state": current_state.value,
                "current_power": current_power,
                "current_current": current_current,
                "total_energy": total_energy
            }
        except Exception as e:
            print(e)

    def configurate_controller(self) -> None:
        self.app = ControllerApplication(ControllerApplication.SCHEMA({
            "start_radio": True,
            "network": {
                "channel": self.chanel,
                "pan_id": 0x1a2b,
                "key": Controller.key_from_hex(self.key)
            },
            "device": {
                "path": self.serial_port,
            }
        }))

    async def start(self) -> None:
        self.shutdown_event = asyncio.Event()
        self.listener = Listener(self.app)
        self.app.add_listener(self.listener)
        await self.app.startup(auto_form=True)
        await self.device_initialized()
        await self.app.permit(60)
        await self.shutdown_event.wait()

    async def device_initialized(self) -> None:
        devices = [Device(application=self.app, ieee=EUI64.convert(data[2]), nwk=data[1])
                   for data in await utils.get_all_devices_adr()]
        [self.listener.device_initialized(device) for device in devices]

    def stop(self) -> None:
        self.app.shutdown(False)
        self.shutdown_event.set()

    async def change_state_device(self, nwk_adr, state) -> bool:
        device = self.app.get_device(nwk=nwk_adr)
        if device:
            if state:
                await device.endpoints[1].on_off.on()
            else:
                await device.endpoints[1].on_off.off()
            attr_dict, _ = await device.endpoints[1].on_off.read_attributes([0x0000])
            current_state = attr_dict.get(0x0000)
            redis = await get_redis()
            address = str(nwk_adr)
            data: bytes = await redis.get(address)
            if data:
                data_dict = json.loads(data.decode())
                data_dict['current_state'] = current_state.value
                await redis.set(address, json.dumps(data_dict).encode())
            return current_state.value

    @staticmethod
    def key_from_hex(key_value) -> t.KeyData:
        bytes_key = bytes.fromhex(key_value)
        return t.KeyData(bytes_key)


controller = Controller()
