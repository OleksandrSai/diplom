from app.app import start_api
import nest_asyncio
import subprocess
import threading
# from app.services.zigbee.orm import ZigbeeOrm
# from app.router.devices.schemas import DevicesDTO, DevicesCreateDTO
# import asyncio


def start_redis():
    try:
        process = subprocess.Popen(['redis-server'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Redis successfully started")
    except Exception as exc:
        print(exc)



def start_project():
    nest_asyncio.apply()
    start_api()


if __name__ == '__main__':
    # zz = ZigbeeOrm()
    # asyncio.run(zz.add_device(nwk_adr=9999, ieee="2132131312"))
    start_project()