from zigpy.zcl.clusters.smartenergy import Metering
from zigpy.zcl.clusters.homeautomation import ElectricalMeasurement
from zigpy.zcl.clusters.general import Identify

import asyncio

class Listener:

    def __init__(self, application):
        self.application = application

    def device_joined(self, device):
        print(f"Device joined: {device}")


    def device_initialized(self, device, *, new=True):
        print(f"new divice  ready {device}")
        # for ep_id, endpoint in device.endpoints.items():
        #
        #     if ep_id == 0:
        #         continue
        #
        #     for cluster in endpoint.in_clusters.values():
        #         cluster.add_context_listener(self)

    def attribute_updated(self, cluster, attribute_id, value, date):
        print(cluster)
        if isinstance(cluster, ElectricalMeasurement):
            name = ElectricalMeasurement.attributes[attribute_id].name
            print(f"name {name} value {value}")
