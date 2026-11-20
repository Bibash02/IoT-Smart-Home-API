from django.core.management.base import BaseCommand
from apps.iot.mqtt_client import MQTTClient

class Command(BaseCommand):
    help = "Start MQTT listener"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting MQTT listener..."))
        mqtt_client = MQTTClient()
        mqtt_client.connect()

        