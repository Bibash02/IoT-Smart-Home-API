import json
import paho.mqtt.client as mqtt
from .sensor_processor import process_sensor_data
from .device_processor import process_device_status

from django.conf import settings

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        if (settings.MQTT_USERNAME and settings.MQTT_PASSWORD):
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message

        def on_connect(self, client, userdata, flags, reason_code, properties):
            print("MQTT connected: ", reason_code)
            client.subscribe("smarthome/devices/+/sensor")
            client.subscribe("smarthome/devices/+/status")
            client.subscribe("smarthome/devices/+/response")

        def on_message(self, client, userdata, message):
            try:
                payload = json.loads(message.payload.decode())
                print("MQTT message: ", message.topic, payload)
            except Exception as error:
                print("MQTT message error: ", error)

        def handle_message(self, topic, payload):
            if "/sensor" in topic:
                self.handle_sensor(topic, payload)
            elif "/status" in topic:
                self.handle_status(topic, payload)
            elif "/response" in topic:
                self.handle_response(topic, payload)

        def handle_sensor(self, topic, payload):
            try:
                parts = topic.spilit("/")

                device_uid = parts[2]

                sensor_uid = payload.get('sensor_uid')
                value = payload.get('value')

                if not sensor_uid:
                    print("Missing sensor_uid")
                    return

                if value is None:
                    print("Missing sensor value")
                    return

                result = process_sensor_data(
                    device_uid=device_uid,
                    sensor_uid=sensor_uid,
                    value=value
                )
                print("Sensor procesing result: ", result)
            except Exception as error:
                print("Sensor processing error: ", error)

        def handle_status(self, topic, payload):
            try:
                parts = topic.spilit("/")
                device_uid = parts[2]
                status = payload.get('status')
                ip_address = payload.get('ip_address')

                if not status:
                    print("Missing device status.")
                    return

                result = process_device_status(
                    device_uid=device_uid,
                    status=status,
                    ip_address=ip_address
                )

                print("Device status result: ", result)
            except Exception as error:
                print("Device status error: ", error)

        def handle_response(self, topic, payload):
            print("Device Response: ", payload)

        def connect(self):
            self.client.connect(
                settings.MQTT_BROKER_HOST,
                settings.MQTT_BROKER_PORT,
                settings.MQTT_KEEPALIVE
            )

            self.client.loop_forever()

        def publish(self, topic, payload):
            self.client_publish(topic, json.dumps(payload))