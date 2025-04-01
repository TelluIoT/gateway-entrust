import asyncio
import csv
import time
from bleak import BleakClient, BleakScanner
import paho.mqtt.client as mqtt

# MQTT client setup
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username="admin", password="admin")

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message published with message ID: {mid}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected disconnection: {rc}")

mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish
mqtt_client.on_disconnect = on_disconnect

mqtt_client.connect("3.254.120.13", 1885, 60)
mqtt_client.loop_start()

# Define the callback for Bluetooth notifications
async def handle_notify(sender, data):
    hex_data = data.hex()
    grouped_data = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]

    # Write grouped data to CSV
    with open('grouped_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(grouped_data)

    # Publish data to MQTT broker
    message = ','.join(grouped_data)
    result = mqtt_client.publish("gateway", message)
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        print("Failed to send message to MQTT broker: ", result.rc)
    else:
        print("Message sent to MQTT broker:", message)

"""
baglanmak istediginiz cihazin bluetooth mac adresini asagidaki addrress
degiskenine yaziniz

K3              : FC:46:EC:71:74:01
K5              : C1:74:BE:E1:26:EB
Multiparameter  : F4:AD:F2:BC:83:44
"""


async def run():
    address = "C1:74:BE:E1:26:EB" # TODO: read from config file (set by MQTT instructions for paired devices)
    command_uuid = "87654321-1234-f393-e0a9-e50e24dcca9e" # what is this?
    response_uuid = "87654321-4321-8765-4321-56789abcdef0" # what is this?

    while True:
        try:
            duration_str = input("Enter desired receive duration (seconds): ")
            duration = int(duration_str)
            if duration > 0:
                break
            else:
                print("Please enter a positive duration.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    async def connect(client, address):
        print(f"Connecting to device: {address}")
        await client.connect(address)
        print("Connected!")

    async def disconnect(client):
        print("Disconnecting from device...")
        await client.disconnect()
        print("Disconnected!")

    async with BleakClient(address, connect_callback=connect, disconnect_callback=disconnect) as client:
        print(f"Connected device: {client.is_connected}")

        try:
            print(f"Sending 0x35 command to UUID: {command_uuid}")
            await client.write_gatt_char(command_uuid, b"\x35")
            print("Command sent successfully!")
        except Exception as e:
            print(f"Error sending command: {e}")

        start_time = time.time()
        while time.time() - start_time < duration:
            await client.start_notify(response_uuid, handle_notify)
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(run())
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
