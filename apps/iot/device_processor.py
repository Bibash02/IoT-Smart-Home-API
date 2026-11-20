from django.utils import timezone
from apps.devices.models import Device
from apps.notifications.services import create_notification

def process_device_status(device_uid, status, ip_address = None):
    try:
        device = Device.objects.get(device_uid = device_uid)
    except Device.DoesNotExist:
        return {
            "success": False,
            "reason": "Device not found."
        }

    status = status.upper()

    if status not in [ "ONLINE", "OFFLINE" ]:
        return {
            "success": False,
            "reason": "Invalid device status."
        }

    was_offline = not device.is_online

    device.is_online = {
        status == "ONLINE"
    }

    device.last_seen = timezone.now()

    if ip_address:
        device.ip_address = ip_address

    device.save(
        update_fields = [
            'is_online',
            "last_seen",
            "ip_address",
            "updated_at"
        ]
    )

    # Device come back online
    if (status == "ONLINE" and was_offline):
        create_notification(
            user = device.user,
            title = "Device Online",
            message=(
                f"Device {device.name}"
                f"is back online"
            ),
            notification_type="DEVICE"
        )

    return {
        "success": True,
        "device": device.name,
        "status": status,
        "last_seen": device.last_seen
    }