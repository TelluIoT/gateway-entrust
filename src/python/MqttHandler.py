"""
MQTT Handler for the gateway application.
Handles MQTT connection, publishing, subscribing, and message processing.
"""

import asyncio
import json
import time
import paho.mqtt.client as mqtt
from typing import Callable, Optional, Dict, Any


class MqttHandler:
    """
    Handles MQTT communication for the gateway.
    """
    def __init__(self, mac_address: str, broker: str, port: int, keep_alive: int = 60):
        """
        Initialize the MQTT handler.
        
        Args:
            mac_address (str): The MAC address of the gateway.
            broker (str): MQTT broker address.
            port (int): MQTT broker port.
            keep_alive (int, optional): Keep alive time in seconds. Defaults to 60.
        """
        self.mac_address = mac_address
        self.broker = broker
        self.port = port
        self.keep_alive = keep_alive
        
        # This will be filled in when credentials are received
        self.username = None
        self.password = None
        self.connected = False
        self.first_connect = True
        self.client = None
        
        # Callback for handling pairing instructions
        self.pairing_callback = None
        
        # Stores the currently paired Bluetooth devices
        self.paired_devices = {}
    
    def set_credentials(self, username: str, password: str):
        """
        Set MQTT credentials.
        
        Args:
            username (str): MQTT username.
            password (str): MQTT password.
        """
        self.username = username
        self.password = password
    
    def set_pairing_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """
        Set callback for handling pairing instructions.
        
        Args:
            callback: Function to call when pairing instructions are received.
        """
        self.pairing_callback = callback
    
    def connect(self) -> bool:
        """
        Connect to the MQTT broker.
        
        Returns:
            bool: True if connection was successful, False otherwise.
        """
        if self.username is None or self.password is None:
            print("Cannot connect to MQTT broker: credentials not set")
            return False
            
        self.client = mqtt.Client()
        self.client.username_pw_set(self.username, self.password)
        
        # Set up callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        
        try:
            self.client.connect(self.broker, self.port, self.keep_alive)
            self.client.loop_start()
            
            # Wait for connection to establish (with timeout)
            start_time = time.time()
            while not self.connected and time.time() - start_time < 10:
                time.sleep(0.1)
                
            return self.connected
            
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")
            return False
    
    def disconnect(self):
        """
        Disconnect from the MQTT broker.
        """
        if self.client is not None:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False
    
    def publish(self, message: str, topic: str = None):
        """
        Publish a message to the MQTT broker.
        
        Args:
            message (str): Message to publish.
            topic (str, optional): Topic to publish to. If None, uses the MAC address as topic.
        """
        if not self.connected:
            print("Cannot publish: not connected to MQTT broker")
            return False
            
        if topic is None:
            topic = self.mac_address
            
        result = self.client.publish(topic, message)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"Failed to publish message: {result.rc}")
            return False
        else:
            print(f"Published message to {topic}: {message}")
            return True
    
    def publish_data(self, device_mac: str, data: Dict[str, Any]):
        """
        Format and publish data from a Bluetooth device.
        
        Args:
            device_mac (str): MAC address of the Bluetooth device.
            data (Dict[str, Any]): Data to publish.
        """
        payload = {
            'gatewayMac': self.mac_address,
            'sensorMac': device_mac,
            'data': data,
            'timestamp': int(time.time()),
            'type': 'measurement',
        }
        
        self.publish(json.dumps(payload))
    
    def subscribe(self, topic: str = None):
        """
        Subscribe to a topic.
        
        Args:
            topic (str, optional): Topic to subscribe to. If None, uses the MAC address + "/1234" as topic.
        """
        if not self.connected:
            print("Cannot subscribe: not connected to MQTT broker")
            return False
            
        if topic is None:
            topic = f"{self.mac_address}" # topic is same as mac address
            
        result = self.client.subscribe(topic)
        if result[0] != mqtt.MQTT_ERR_SUCCESS:
            print(f"Failed to subscribe to {topic}: {result[0]}")
            return False
        else:
            print(f"Subscribed to {topic}")
            return True
    
    # Callback methods
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker successfully.")
            self.connected = True
            
            # Subscribe to the topic
            self.subscribe()
            
        
            if self.first_connect:
                # Send connected message on first connect (debug purposes or request sensor list)
                # self.publish("connected!")
                self.first_connect = False
                
        else:
            print(f"Failed to connect to MQTT broker, return code: {rc}")
            self.connected = False
    
    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print(f"Unexpected disconnection: {rc}")
        self.connected = False
    
    def _on_message(self, client, userdata, msg):
        """
        Handle incoming MQTT messages.
        """
        try:
            message_str = msg.payload.decode()
            print(f"Message received on {msg.topic}: {message_str}")
            
            # Try to parse message as JSON
            try:
                message = json.loads(message_str)
                
                # Handle pairing/unpairing instructions
                if 'type' in message:
                    if message['type'] == 'pair' and self.pairing_callback is not None:
                        self.pairing_callback(message)
                    elif message['type'] == 'unpair' and self.pairing_callback is not None:
                        self.pairing_callback(message)
            except json.JSONDecodeError:
                print("Received message is not valid JSON")
                
        except Exception as e:
            print(f"Error processing message: {e}")
