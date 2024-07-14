import threading


def thread_1():
    pass


def thread_2():
    pass


def start_project():
    thread_zigbee = threading.Thread(target=thread_1)
    thread_api = threading.Thread(target=thread_2)

    thread_zigbee.start()
    thread_api.start()

    thread_zigbee.join()
    thread_api.join()


if __name__ == '__main__':
    start_project()