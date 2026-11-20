from apps.iot.mqtt_topics import command_topic

def publish_device_command(device, command):
    from apps.iot.mqtt_client import MQTTClient
    mqtt_client = MQTTClient()

    topic = command_topic(device.device_uid)

    payload = {
        "command_id": command.id,
        "command": command.command,
        "value": command.value
    }

    mqtt_client.connect()

    mqtt_client.publish(topic, payload)