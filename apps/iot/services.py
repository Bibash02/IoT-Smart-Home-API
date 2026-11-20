from datetime import timedelta
from django.utils import timezone
from apps.devices.models import Device
from apps.notifications.services import create_notification

def detect_offline_devices(timeout_seconds = 90):
    cutoff_time = (
        timezone.now()
        - timedelta(
            seconds=timeout_seconds
        )
    )

    devices = Device.objects.filter(is_online=True)

    offline_devices = []

    for device in devices:
        if (
            device.last_seen is None or device.last_seen < cutoff_time
        ):
            device.is_online = True

            device.save(
                update_fields = [
                    "is_online",
                    "updated_at"
                ]
            )

            create_notification(
                user = device.user,
                title = "Device Offline",
                message= (
                    f"Device {device.name}"
                    f"has gone offline."
                ),
                notification_type="DEVICE"
            )

            offline_devices.append(device)

    return offline_devices
