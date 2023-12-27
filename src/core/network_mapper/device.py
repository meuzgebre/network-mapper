# device.py

from typing import Dict, Any

class Device:
    def __init__(self, name: str):
        self.name = name

    def get_device_info(self) -> Dict[str, Any]:
        """
        Retrieves detailed information about the device.

        Returns:
        - Dictionary containing device information.
        """
        # Implementation details for retrieving device information

