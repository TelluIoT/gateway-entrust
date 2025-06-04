"""
Main entry point for the gateway application.
Manages the gateway state machine and coordinates MQTT and Bluetooth communication.
"""

import asyncio
import json
import time
import requests
from typing import Dict, Optional, Any

# Import configuration
import config as config

# Import handlers
from MqttHandler import MqttHandler
from BluetoothAdapter import BluetoothAdapter


class GatewayState:
    """Enum-like class for gateway states"""
    UNREGISTERED = "unregistered"
    REGISTERED = "registered"
    CONNECTED = "connected"

queue = asyncio.Queue()  # Global queue for events
attempts = 0  # Global variable to track registration attempts


class Gateway:
    """
    Main gateway class that manages the state machine and coordinates components.
    """
    def __init__(self):
        self.mac_address = config.GATEWAY_MAC
        self.state = config.INITIAL_STATE # default state
        
        # Credentials and secret (would be stored persistently in production)
        self.secret = config.MOCK_SECRET
        self.mqtt_username = config.GATEWAY_MAC
        self.mqtt_password = config.MOCK_PASSWORD
        
        # Handlers
        self.mqtt_handler = MqttHandler(
            queue,
            self.mac_address,
            config.MQTT_BROKER,
            config.MQTT_PORT,
            config.MQTT_KEEPALIVE
        )
        
        self.ble_adapter = BluetoothAdapter()
        self.ble_adapter.inject_mqtt_handler(self.mqtt_handler)
        
        # Set up callbacks
        # self.mqtt_handler.set_pairing_callback(self.handle_instruction)
        
        # For clean shutdown
        self.running = True

        self.isFirstBoot = True   # Global variable to track if this is the first boot
        self.heartbeat_counter = 0 


    # def get_event_loop(self):
    #     """
    #     Get the current event loop or create a new one if needed.
        
    #     Returns:
    #         asyncio.AbstractEventLoop: The event loop
    #     """
    #     try:
    #         # Try to get the current event loop
    #         return asyncio.get_event_loop()
    #     except RuntimeError:
    #         # If there's no event loop in this thread, create a new one
    #         loop = asyncio.new_event_loop()
    #         asyncio.set_event_loop(loop)
    #         return loop
        
    async def register_gateway(self) -> bool:
        """
        Register the gateway with the server.
        
        Returns:
            bool: True if registration was successful, False otherwise.
        """
        print(f"Attempting to register gateway {self.mac_address}...")
        
        try:
            response = requests.get(
                f"{config.REGISTRATION_ENDPOINT}?macAddress={self.mac_address}",
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print("Registration successful")
                
                # Assuming the server returns JSON with a secret
                try:
                    response_data = response.json()
                    if 'secret' in response_data:
                        self.secret = response_data['secret']
                    else:
                        # For backward compatibility - in the example code we see concatenation with 'abcd'
                        self.secret = self.mac_address + 'abcd'
                        
                    print(f"Received secret for gateway")
                    return True
                except ValueError:
                    print("Registration response was not valid JSON")
                    # Fallback for backward compatibility
                    self.secret = self.mac_address + 'abcd'
                    return True
                    
            else:
                print(f"Registration failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Registration request failed: {e}")
            return False
            
    async def get_mqtt_credentials(self) -> bool:
        """
        Get MQTT credentials from the server.
        
        Returns:
            bool: True if credentials were successfully retrieved, False otherwise.
        """
        if self.secret is None:
            print("Cannot get MQTT credentials: gateway not registered (no secret)")
            return False
            
        print(f"Requesting MQTT credentials for gateway {self.mac_address}...")
        
        try:
            response = requests.get(
                f"{config.GET_CREDENTIALS_ENDPOINT}?macAddress={self.mac_address}&secret={self.secret}",
                timeout=10
            )
            
            if response.status_code == 200:
                print("Credentials request successful")
                
                # Extract credentials from response
                try:
                    response_data = response.json()
                    if 'username' in response_data and 'password' in response_data:
                        self.mqtt_username = response_data['username']
                        self.mqtt_password = response_data['password']
                    else:
                        # For backward compatibility - in the example code we see concatenation with '1234'
                        self.mqtt_username = self.mac_address
                        self.mqtt_password = self.mac_address + '1234'
                        
                    print(f"Received MQTT credentials")
                    return True
                except ValueError:
                    print("Credentials response was not valid JSON")
                    # Fallback for backward compatibility
                    self.mqtt_username = self.mac_address
                    self.mqtt_password = self.mac_address + '1234'
                    return True
                    
            else:
                print(f"Credentials request failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Credentials request failed: {e}")
            return False
            
    async def connect_mqtt(self) -> bool:
        """
        Connect to the MQTT broker.
        
        Returns:
            bool: True if connection was successful, False otherwise.
        """
        if self.mqtt_username is None or self.mqtt_password is None:
            print("Cannot connect to MQTT: missing credentials")
            return False
            
        # Set credentials in MQTT handler
        self.mqtt_handler.set_credentials(self.mqtt_username, self.mqtt_password)
        
        # Connect to broker
        return self.mqtt_handler.connect()
    
    async def handle_instruction(self, instruction: Dict[str, Any]):
        """
        Handle pairing instructions received from MQTT.
        
        Args:
            instruction (Dict[str, Any]): Pairing instruction.
        """
        try:
            instruction_type = instruction.get('type')

            if instruction_type == 'pair':
                print(f"Received pairing instruction: {instruction}")
                await self.ble_adapter.pair_device(instruction)
                
            elif instruction_type == 'unpair':
                print(f"Received unpairing instruction: {instruction}")
                await self.ble_adapter.unpair_device(instruction)
            
            elif instruction_type == 'scan':
                print(f"Received scan instruction: {instruction}")
                await self.ble_adapter.scan_devices(config.BLE_SCAN_TIMEOUT)

            elif instruction_type == 'read':
                print(f"Received read instruction: {instruction}")
                address = instruction['address']
                await self.ble_adapter.read_data(address)

            elif instruction_type == 'sensorlist':
                print(f"Received sensorlist instruction: {instruction}")
                
                toPair = instruction['sensors']
                for sensor in toPair:
                    if not self.ble_adapter.is_device_connected(sensor['address']):
                        successPaired = await self.ble_adapter.pair_device(sensor)

                        if successPaired is True:
                            print(f"Successfully paired sensor {sensor['address']}")
                        else:
                            print(f"Failed to pair sensor {sensor['address']}")

           

            else:
                print(f"Unknown instruction type: {instruction_type}")
                
        except Exception as e:
            if config.DEBUG_MODE == True:
                raise e
            
            print(f"Error handling pairing instruction: {e}")

    async def run(self):
        """
        Run the gateway state machine.
        """
        print(f"Starting gateway {self.mac_address}")
        
        while self.running:
            # try:
                # State machine
                if self.state == GatewayState.UNREGISTERED and attempts < config.MAX_REGISTRATION_ATTEMPTS:
                    print("Gateway is unregistered. Attempting to register...")
                    if await self.register_gateway():
                        self.state = GatewayState.REGISTERED
                    else:
                        # Wait before retrying registration
                        attempts += 1
                        await asyncio.sleep(10)
                        
                elif self.state == GatewayState.REGISTERED and attempts < config.MAX_REGISTRATION_ATTEMPTS:
                    print("Gateway is registered. Requesting MQTT credentials...")
                    if await self.get_mqtt_credentials():
                        if await self.connect_mqtt():
                            self.state = GatewayState.CONNECTED
                        else:
                            # Wait before retrying MQTT connection
                            attempts += 1
                            await asyncio.sleep(5)
                    else:
                        # Wait before retrying credential request
                        attempts += 1
                        await asyncio.sleep(10)
                        
                elif self.state == GatewayState.CONNECTED:
                    # Main operational state - periodically check MQTT connection
                    if not self.mqtt_handler.connected:
                        print("MQTT connection lost. Reconnecting...")
                        if not await self.connect_mqtt():
                            # Fall back to registered state if connection fails
                            self.state = GatewayState.REGISTERED

                    if self.isFirstBoot is True:
                        print("First boot detected. Scanning for devices...")
                        payload = {
                            'from': self.mac_address,
                            'timestamp': int(time.time()),
                            'type': "getsensorlist",
                        }
        
                        self.mqtt_handler.publish(json.dumps(payload))
                        self.isFirstBoot = False
                   
                    try:
                        # Process any events in the queue
                        while True:
                            instruction = queue.get_nowait()
                            print(f"Processing instruction: {instruction}")
                            await self.handle_instruction(instruction)
                            queue.task_done()  # Mark the instruction as processed
                            # TODO: handle different types of instructions - rename to handle_instruction(?)
                       
                    except asyncio.QueueEmpty:
                        # nothing to process
                        pass

                    if self.heartbeat_counter == 12:  # every 1 minutes
                        print("Sending heartbeat...")
                        
                        # Get connected sensors and their status
                        sensors = []
                        for address, client in self.ble_adapter.connected_devices.items():
                            sensors.append({
                                "address": address,
                                "ispaired": client.is_connected
                            })
                        
                        payload = {
                            'from': self.mac_address,
                            'timestamp': int(time.time()),
                            'type': "heartbeat",
                            'gatewayMac': self.mac_address,
                            'sensorlist': json.dumps(sensors)  # Directly include the sensor list as a JSON array
                        }
                        self.mqtt_handler.publish(json.dumps(payload))
                        self.heartbeat_counter = 0
                    
                    # Main loop delay
                    self.heartbeat_counter += 1
                    await asyncio.sleep(5)
                    
            # except Exception as e:
            #     print(f"Error in main loop: {e}")
            #     await asyncio.sleep(10)
                
    def stop(self):
        """
        Stop the gateway and clean up resources.
        """
        print("Stopping gateway...")
        self.running = False
        
        # Disconnect MQTT
        if self.mqtt_handler is not None:
            self.mqtt_handler.disconnect()
            
        print("Gateway stopped")

async def main():
    gateway = Gateway()

    # Debug - run with no error handling
    await gateway.run() # runs a state machine - does not return until stopped
    
    # try:
    #     await gateway.run() # runs a state machine - does not return until stopped
    # except Exception as e:
    #     print(f"Uncaught exception: {e}")
    # finally:
    #     gateway.stop()


if __name__ == "__main__":
    asyncio.run(main()) # initialize the event loop
