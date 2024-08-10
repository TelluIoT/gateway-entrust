from bleak import BleakClient

from i_bluetooth_adapter import IBluetoothAdapter;

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