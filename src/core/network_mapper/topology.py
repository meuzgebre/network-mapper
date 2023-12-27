# topology.py

from typing import List

class Topology:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        """
        Adds a device to the topology.

        Args:
        - device: An instance of the Device class.
        """
        self.devices.append(device)

    def remove_device(self, device):
        """
        Removes a device from the topology.

        Args:
        - device: An instance of the Device class.
        """
        self.devices.remove(device)

    def get_devices(self) -> List:
        """
        Retrieves a list of devices in the topology.

        Returns:
        - List of Device objects.
        """
        return self.devices

