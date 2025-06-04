"""
Configuration file for the gateway application.
"""

INITIAL_STATE = "connected"  # Initial state of the gateway: "unregistered" | "registered" | "connected"
MAX_REGISTRATION_ATTEMPTS = 10
 
# Gateway identification
GATEWAY_MAC = "B827EBB63381"  # Replace with your actual MAC address or device ID
MOCK_SECRET = "B827EBB63381abcd"
MOCK_PASSWORD = "B827EBB633811234"

# HTTP Endpoints
REGISTRATION_ENDPOINT = "http://34.240.4.8:3010/register"  # Replace with actual registration endpoint
GET_CREDENTIALS_ENDPOINT = "http://34.240.4.8:3010/getCredentials"  # Replace with actual credentials endpoint

# MQTT Configuration
MQTT_BROKER = "34.240.4.8"  # Replace with actual MQTT broker address
MQTT_PORT = 1885  # Replace with actual MQTT port
MQTT_KEEPALIVE = 60  # Keep alive time in seconds

# Bluetooth Configuration
BLE_SCAN_TIMEOUT = 30.0  # Scanning timeout in seconds
BLE_MEASUREMENT_DURATION = 10  # Measurement duration in seconds

DEBUG_MODE = True
