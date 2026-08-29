from django.core.management.base import BaseCommand
from iot.services import detect_offline_devices

class Command(BaseCommand):
    help = "Check IoT device heartbeat."

    def handle(self, *args, **options):
        devices = detect_offline_devices()

        for device in devices:
            self.stdout.write(
                self.style.SUCCESS(
                    "Device check completed."
                )
            )