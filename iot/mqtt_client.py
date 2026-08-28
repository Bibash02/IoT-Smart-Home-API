import json
import paho.mqtt.client as mqtt

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
            print("Sensor data: ", payload)

        def handle_status(self, topic, payload):
            print("Device Status: ", payload)

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