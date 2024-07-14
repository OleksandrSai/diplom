import threading
from zigbee.сontroller import Controller
from api.app import start_api


def start_project():
    zigbee_controller = Controller()
    thread_zigbee = threading.Thread(target=zigbee_controller.start_controller)
    thread_api = threading.Thread(target=start_api)

    thread_zigbee.start()
    thread_api.start()

    thread_zigbee.join()
    thread_api.join()


if __name__ == '__main__':
    start_project()