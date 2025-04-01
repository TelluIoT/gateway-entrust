import paho.mqtt.client as mqtt
import time
from config import mqtt_hostname, mqtt_port

class MQTTClient:
    def __init__(self, sensorMacAddress: str):
        self._client = mqtt.Client()
        self._topic = sensorMacAddress
        self._username = sensorMacAddress
        self._password = sensorMacAddress + '1234' #TODO: read from file instead of computing
        self._broker_address = mqtt_hostname
        self._broker_port = mqtt_port # configured MQTT port on RabbitMQ component
        self._keep_alive = 60
        self._text_file = "attached_sensors.txt"
        
        # Set up callbacks
        self._client.on_connect = self.on_connect
        self._client.on_disconnect = self.on_disconnect
        

    def connect(self):
        print(f"Connecting to MQTT broker at {self._broker_address}:{self._broker_port}...")
        print(f"Connecting to MQTT broker, username {self._username}:{self._password}...")
        self._client.username_pw_set(self._username, self._password)
        try:
            self._client.connect(self._broker_address, self._broker_port, self._keep_alive)
            print('Successfully called client.connect')
            self._client.loop_start()  # Start the loop to process network traffic and dispatch callbacks
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 30 seconds...")
            time.sleep(30)
            self.connect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker successfully.")
            self._client.subscribe(self._topic)
            print(f"Subscribed to topic '{self._topic}'")
        else:
            print(f"Failed to connect, return code {rc}. Retrying in 30 seconds...")
            time.sleep(30)
            self.connect()

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection. Reconnecting in 30 seconds...")
            time.sleep(30)
            self.connect()

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        print("Message received:", message)
        
        # Write the message to a text file
        with open(self._text_file, "a") as file:
            file.write(f"{message}\n")

    def publish(self, message):
        self._client.publish(self._topic, message)
        print(f"Message '{message}' published to topic '{self._topic}'")

    def subscribe(self):
        print('hit "subscribe" method in mqttClient')
        self._client.subscribe(self._topic)
        self._client.on_message = self.on_message
        print(f"subscribed to {self._topic}")

    def disconnect(self):
        self._client.loop_stop()  # Stop the loop
        self._client.disconnect()
        print("Disconnected from the MQTT broker.")

