import asyncio
from zigpy_znp.zigbee.application import ControllerApplication
from listner import Listener
import zigpy_znp.types as t


class Controller:
    def __init__(self):
        self.app = None
        self.pan_id = 1996
        self.chanel = 15
        self.serial_port = "COM4"
        self.key = "99ffff33445566778899aabbccd11111"
        self.configurate_controller()

    @staticmethod
    def key_from_hex(key_value) -> t.KeyData:
        bytes_key = bytes.fromhex(key_value)
        return t.KeyData(bytes_key)

    def configurate_controller(self):
        self.app = ControllerApplication(ControllerApplication.SCHEMA({
            "database_path": "./zigbee.db",
            "network": {
                "channel": self.chanel,
                "pan_id": self.pan_id,
                "key": Controller.key_from_hex(self.key)
            },
            "device": {
                "path": self.serial_port,
            }
        }))

    async def start(self):
        listener = Listener(self.app)
        self.app.add_listener(listener)

        await self.app.startup(auto_form=True)

        for device in self.app.devices.values():
            listener.device_initialized(device, new=False)

        await self.app.permit(60)

        await asyncio.sleep(60)

        await asyncio.get_running_loop().create_future()

    def start_controller(self):
        asyncio.run(self.start())


if __name__ == "__main__":
    controller = Controller()
    controller.start_controller()