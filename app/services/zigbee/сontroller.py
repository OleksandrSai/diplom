import asyncio
import json
from zigpy_znp.zigbee.application import ControllerApplication
from zigpy.types import t
from config import settings
from .listener import Listener
import async_timeout
from zigpy import types as t


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

    @staticmethod
    def key_from_hex(key_value) -> t.KeyData:
        bytes_key = bytes.fromhex(key_value)
        return t.KeyData(bytes_key)

    async def discover_attributes(self, device, endpoint_id, cluster_id):
        cluster = device.endpoints[endpoint_id].clusters[cluster_id]
        attributes = await cluster.discover_attributes()
        return attributes

    async def read_attributes(self, cluster, attribute_ids):
        try:
            async with async_timeout.timeout(10):
                result = await cluster.read_attributes(attribute_ids)
                return result[0]  # Возвращаем только первую часть кортежа, содержащую атрибуты
        except asyncio.TimeoutError:
            print(f"Timeout while reading attributes {attribute_ids} from cluster {cluster.cluster_id}")
            return {}
        except Exception as e:
            print(f"Error reading attributes {attribute_ids} from cluster {cluster.cluster_id}: {e}")
            return {}

    async def read_interval(self):
        try:
            device = self.app.get_device(nwk=0xFF15)
            attribute_ids = [0x0000]  # Current Summation Delivered and Instantaneous Demand
            endpoint = device.endpoints[1]
            attr_dict, _ = await endpoint.smartenergy_metering.read_attributes(attribute_ids)
            total_energy = attr_dict.get(0x0000)  # Total energy in kWh
            if total_energy:
                print(total_energy * 10000000)
            print(f"Total Energy: {total_energy * 100} kWh")
            attribute_ids = [0x050B]
            attr_dict, _ = await endpoint.electrical_measurement.read_attributes(attribute_ids)
            current_power = attr_dict.get(0x050B, 0)
            print(f"Current Power: {current_power} W")
            dict_data = {
                "current_power": current_power,
                "total_energy": total_energy
            }
            res = json.dumps(dict_data)
            return res
        except Exception as e:
            print(e)

    def configurate_controller(self):
            self.app = ControllerApplication(ControllerApplication.SCHEMA({
                "start_radio": True,
                "network": {
                    "channel": self.chanel,
                    "pan_id": 0x1a2b,  # PAN ID
                    "key": Controller.key_from_hex(self.key)
                },
                "device": {
                    "path": self.serial_port,
                }
            }))

    async def start(self):
        self.shutdown_event = asyncio.Event()
        self.listener = Listener(self.app)
        self.app.add_listener(self.listener)
        await self.app.startup(auto_form=True)
        for device in self.app.devices.values():
            self.listener.device_initialized(device, new=True)

        await self.app.permit(60)

        await self.shutdown_event.wait()

    def stop(self):
        self.app.shutdown(False)
        self.shutdown_event.set()

    async def turn_on_device(self, device_id):
        device = self.app.get_device(nwk=device_id)
        if device:
            await device.endpoints[1].on_off.on()

    async def turn_off_device(self, device_id):
        device = self.app.get_device(nwk=device_id)
        if device:
            await device.endpoints[1].on_off.off()
