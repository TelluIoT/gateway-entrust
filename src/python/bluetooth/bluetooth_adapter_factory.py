from typing import Type;
from adapter_mock import AdapterMock;

class BluetoothAdapterFactory:
    @staticmethod
    def create_adapter(adapter_type: str, macAddress: str):
        if adapter_type == "mock":
            return AdapterMock(macAddress)
        else:
            raise ValueError("Unsupported adapter type")
