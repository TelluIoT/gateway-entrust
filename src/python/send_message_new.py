import argparse
import asyncio
from pathlib import Path

import config
from bluetooth import BluetoothAdapterFactory
from MqttHandler import MqttHandler


def read_text_file(path: Path, fallback: str = "") -> str:
    if not path.exists():
        return fallback
    return path.read_text(encoding="utf-8").strip()


async def main(send_once: bool, interval: float, value: str):
    base_dir = Path(__file__).resolve().parent
    sensor_mac = read_text_file(base_dir / "mock_mac.txt", "MOCK_SENSOR")
    gateway_mac = config.GATEWAY_MAC
    test_topic = f"{gateway_mac}.test"

    adapter = BluetoothAdapterFactory.create_adapter("mock", sensor_mac)
    await adapter.connect()

    mqtt_handler = MqttHandler(
        asyncio.Queue(),
        gateway_mac,
        config.MQTT_BROKER,
        config.MQTT_PORT,
        config.MQTT_KEEPALIVE,
    )
    mqtt_handler.set_credentials(gateway_mac, config.MOCK_PASSWORD)
    mqtt_handler.set_auto_subscribe_on_connect(False)

    if not mqtt_handler.connect():
        await adapter.disconnect()
        raise RuntimeError("Failed to connect to MQTT broker")

    try:
        while True:
            data = value

            print(f"Publishing test measurement to topic {test_topic}")
            mqtt_handler.publish_data(adapter.macAddress, data, topic=test_topic)
            print(f"Published dummy measurement for sensor {adapter.macAddress}")

            if send_once:
                break

            await asyncio.sleep(interval)
    finally:
        await adapter.disconnect()
        mqtt_handler.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send dummy sensor messages through the gateway MQTT flow.")
    parser.add_argument("--once", action="store_true", help="Send one dummy message and exit.")
    parser.add_argument("--interval", type=float, default=5.0, help="Seconds between messages when not using --once.")
    parser.add_argument("--value", default="120/80", help="Small readable dummy value to publish.")
    arguments = parser.parse_args()
    asyncio.run(main(arguments.once, arguments.interval, arguments.value))