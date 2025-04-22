import asyncio
from bluetooth import BluetoothAdapterFactory
from mqttNew import MQTTClient;
import time


async def main():
    # Instantiate the Bluetooth adapter using the factory
    with open ("mock_mac.txt", 'r') as file:
        mac_address = file.read()

    adapter = BluetoothAdapterFactory.create_adapter("mock", mac_address)

    # Connect to the Bluetooth device
    await adapter.connect()

    # Read data from the device
    data = await adapter.read_data()

    # Forward the read data to MQTT broker
    print('Macaddress: ', mac_address)
    mqtt_client = MQTTClient(mac_address)
    mqtt_client.connect()
    # mqtt_client.publish(data)

    mqtt_client.subscribe()
        
    # Keep the script running to subscribe
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mqtt_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())