"""
Bluetooth adapter for the gateway application using Bleak.
Handles BLE device scanning, connection, and data reception.
"""

import asyncio
import json
from typing import Dict, List, Optional, Callable, Any
from bleak import BleakClient, BleakScanner
import time
import config as config
from MqttHandler import MqttHandler

class DataCache:

    def __init__(self):
        self.cached_data = []
    
    def get_data(self) -> str:
        return ','.join(self.cached_data)

    async def handle_notify(self, sender, data):
        hex_data = data.hex()
        grouped_data = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]

        # # Write grouped data to CSV
        # with open('grouped_data.csv', 'a', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(grouped_data)
        print("grouped data", grouped_data)
        
        message = ','.join(grouped_data)

        self.cached_data.append(message)


class BluetoothAdapter:
    """
    Handles Bluetooth Low Energy communication for the gateway.
    """
    def __init__(self):
        """
        Initialize the Bluetooth adapter.
        """
        self.connected_devices = {}  # MAC address -> BleakClient
        self.mqtt_handler: MqttHandler = None
        self.notification_callbacks = {}  # MAC address -> characteristic UUID -> callback
        
    def inject_mqtt_handler(self, mqtt_handler: MqttHandler):
        """
        Inject the MQTT handler for publishing received data.
        
        Args:
            mqtt_handler: The MQTT handler instance.
        """
        self.mqtt_handler = mqtt_handler


    async def read_data(self, address: str):
        command_uuid = "87654321-1234-f393-e0a9-e50e24dcca9e"
        RESPONSE_UUID = "87654321-4321-8765-4321-56789abcdef0"

        client = self.connected_devices[address]

        try:
            print(f"Sending 0x35 command to UUID: {command_uuid}")
            await client.write_gatt_char(command_uuid, b"\x35")
            print("Command sent successfully!")
        except Exception as e:
            print(f"Error sending command: {e}")

        dataCache = DataCache()

        start_time = time.time()
        while (time.time() - start_time) < config.BLE_MEASUREMENT_DURATION:
            await client.start_notify(RESPONSE_UUID, dataCache.handle_notify) # this command will trigger the simulated measurement generation in the kardinBLU, making it generate measurements.
            await asyncio.sleep(1)
        
        await client.stop_notify(RESPONSE_UUID)

        print("Data reading complete.")

        # Publish collected data to MQTT broker
        dataList = dataCache.get_data()
        self.mqtt_handler.publish_data(address, dataList)
        
    async def scan_devices(self, timeout: float = 5.0) -> List[Dict[str, Any]]:
        """
        Scan for BLE devices.
        
        Args:
            timeout (float): Scan timeout in seconds.
            
        Returns:
            List[Dict[str, Any]]: List of detected devices with their details.
        """
        print(f"Scanning for BLE devices (timeout: {timeout}s)...")
        devices = await BleakScanner.discover(timeout=timeout)
        
        device_list = []
        for device in devices:
            device_info = {
                "address": device.address,
                "name": device.name or "Unknown",
                "rssi": device.rssi,
            }
            device_list.append(device_info)
            print(f"Found device: {device.name or 'Unknown'} ({device.address}) - RSSI: {device.rssi}")
        
        print(f"Scan complete. Found {len(device_list)} devices.")
        return device_list
    
    def is_device_connected(self, address: str) -> bool:
        """
        Check if a device is connected.
        
        Args:
            address (str): MAC address of the device.
            
        Returns:
            bool: True if the device is connected, False otherwise.
        """
        return address in self.connected_devices
    
        
    async def connect_device(self, address: str) -> bool:
        """
        Connect to a BLE device.
        
        Args:
            address (str): MAC address of the device.
            
        Returns:
            bool: True if connection was successful, False otherwise.
        """
        if address in self.connected_devices and self.connected_devices[address].is_connected:
            print(f"Device {address} is already connected")
            return True
            
        try:
            print(f"Connecting to device: {address}")
            client = BleakClient(address)
            await client.connect()
            
            if client.is_connected:
                self.connected_devices[address] = client
                print(f"Connected to {address}")
                return True
            else:
                print(f"Failed to connect to {address}")
                return False
                
        except Exception as e:
            print(f"Error connecting to {address}: {e}")
            return False
            
    async def disconnect_device(self, address: str) -> bool:
        """
        Disconnect from a BLE device.
        
        Args:
            address (str): MAC address of the device.
            
        Returns:
            bool: True if disconnection was successful, False otherwise.
        """
        if address not in self.connected_devices:
            print(f"Device {address} is not connected")
            return True
            
        client = self.connected_devices[address]
        try:
            await client.disconnect()
            del self.connected_devices[address]
            print(f"Disconnected from {address}")
            return True
        except Exception as e:
            print(f"Error disconnecting from {address}: {e}")
            return False
    
    async def pair_device(self, device_info):
        """
        Handle pairing with a new device based on instructions.
        
        Args:
            device_info (Dict): Device information including MAC address and configuration.
        """
        if 'address' not in device_info:
            print("Cannot pair: Missing device address in pairing information")
            return False
        
        address = device_info['address']
        
        # Connect to the device
        connected = await self.connect_device(address)
        if not connected:
            return False
            
        # If device-specific configuration is provided
        if 'config' in device_info:
            config = device_info['config']
            
            # Handle configuration (this would be device-specific)
            if 'notify_characteristics' in config:
                for char_uuid in config['notify_characteristics']:
                    await self.start_notify(address, char_uuid)
                    
            # Write initial commands if needed
            if 'initial_commands' in config:
                for cmd in config['initial_commands']:
                    char_uuid = cmd.get('characteristic')
                    data = bytes.fromhex(cmd.get('data', ''))
                    if char_uuid:
                        await self.write_characteristic(address, char_uuid, data)
        
        return True
    
    async def unpair_device(self, device_info):
        """
        Handle unpairing of a device.
        
        Args:
            device_info (Dict): Device information including MAC address.
        """
        if 'address' not in device_info:
            print("Cannot unpair: Missing device address in unpairing information")
            return False
        
        address = device_info['address']
        
        # Stop all notifications first
        if address in self.notification_callbacks:
            for char_uuid in list(self.notification_callbacks[address].keys()):
                await self.stop_notify(address, char_uuid)
        
        # Disconnect from the device
        return await self.disconnect_device(address)
