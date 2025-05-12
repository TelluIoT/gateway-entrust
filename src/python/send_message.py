import asyncio
from bluetooth import BluetoothAdapterFactory
from mqtt import MQTTClient;
import time
import json


async def main():
    # Instantiate the Bluetooth adapter using the factory
    with open ("mock_mac.txt", 'r') as file:
        mac_address = file.read()
    
    with open ("mock_secret.txt", 'r') as file:
        secret = file.read()

    adapter = BluetoothAdapterFactory.create_adapter("mock", mac_address)

    # Connect to the Bluetooth device
    await adapter.connect()

    # Read data from the device
    data = await adapter.read_data()

    # Forward the read data to MQTT broker
    print('Macaddress: ', mac_address)
    mqtt_client = MQTTClient(mac_address)
    mqtt_client.connect()

    # TODO: hash with the secret as salt? Decrypt when received in TelluCare
    payload = {
        'gatewayMac': mac_address,
        'sensorMac': adapter.macAddress,
        'value': data,
        'type': 'measurement',
        'secret': secret,
    }

    jsonPayload = json.dumps(payload)
    
    mqtt_client.publish(jsonPayload)

    mqtt_client.subscribe()
        
    # Keep the script running to subscribe
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mqtt_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())