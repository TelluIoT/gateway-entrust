import asyncio
from bluetooth_adapter_factory import BluetoothAdapterFactory


async def main():
    # Instantiate the Bluetooth adapter using the factory
    adapter = BluetoothAdapterFactory.create_adapter("mock", "XX:XX:XX:XX:XX:XX")

    # Connect to the Bluetooth device
    await adapter.connect()

    # Read data from the device
    await adapter.read_data()

    # Write data to the device
    await adapter.write_data(b"Hello Bluetooth!")

    # Disconnect from the device
    await adapter.disconnect()

    # This is a comment

if __name__ == "__main__":
    asyncio.run(main())