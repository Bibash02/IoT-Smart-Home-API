import json
import paho.mqtt.client as mqtt
from django.conf import settings

def publish_command(device_uid, command_id, command, value):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    if (settings.MQTT_USERNAME and settings.MQTT_PASSWORD):
        client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

    client.connect(
        settings.MQTT_BROKER_HOST,
        settings.MQTT_BROKER_PORT,
        settings.MQTT_KEEPALIVE
    )

    topic = (
        f"smarthome/devices/"
        f"{device_uid}/command"
    )

    payload = {
        "command_id": command_id,
        "command": command,
        "value": value
    }

    client.publish(
        topic,
        json.dumps(payload)
    )

    client.disconnect()

    