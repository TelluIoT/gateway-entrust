from bleak import BleakClient
import asyncio
# from typing import Type;
from abc import ABC, abstractmethod

class IBluetoothAdapter(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def read_data(self):
        pass

    @abstractmethod
    async def write_data(self, data):
        pass


class BluetoothAdapterFactory:
    @staticmethod
    def create_adapter(adapter_type: str, macAddress: str):
        if adapter_type == "mock":
            return AdapterMock(macAddress)
        else:
            raise ValueError("Unsupported adapter type")

# adapters
class AdapterActualBluetooth(IBluetoothAdapter):
    def __init__(self, macAddress: str):
        self.macAddress = macAddress
        self.client = BleakClient(self.macAddress)

    async def connect(self):
        print(f"Connecting to {self.macAddress}...")
        await self.client.connect()
        print("Connected.")

    async def disconnect(self):
        print(f"Disconnecting from {self.macAddress}...")
        await self.client.disconnect()
        print("Disconnected.")

    async def read_data(self):
        # For demonstration, let's assume we read some mock data
        print("Reading data from device...")
        data = await self.client.read_gatt_char("00002a37-0000-1000-8000-00805f9b34fb")
        print(f"Data received: {data}")
        return data

    async def write_data(self, data):
        # For demonstration, let's assume we write some mock data
        print(f"Writing data to device: {data}")
        await self.client.write_gatt_char("00002a37-0000-1000-8000-00805f9b34fb", data)
        print("Data written.")


class AdapterMock(IBluetoothAdapter):
    def __init__(self, macAddress: str):
        self.macAddress = macAddress

    async def connect(self):
        print(f"Connecting to {self.macAddress}...")
        await asyncio.sleep(1)
        print("Connected.")

    async def disconnect(self):
        print(f"Disconnecting from {self.macAddress}...")
        await asyncio.sleep(1)
        print("Disconnected.")

    async def read_data(self):
        print("Reading data from device...")
        await asyncio.sleep(1)
        data = "This is dummy data!!"
        print(f"Data received: {data}")
        return data

    async def write_data(self, data):
        print(f"Writing data to device: {data}")
        await asyncio.sleep(1)
        print("Data written.")

# end adapters



