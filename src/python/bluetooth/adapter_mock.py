import asyncio
from i_bluetooth_adapter import IBluetoothAdapter;

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