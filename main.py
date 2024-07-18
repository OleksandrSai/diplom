import threading
from zigbee.сontroller import Controller
from api.app import start_api
import time

def start_project():
   start_api()


if __name__ == '__main__':
    start_project()