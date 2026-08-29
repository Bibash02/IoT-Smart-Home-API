from django.utils import timezone
from devices.models import Device

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

    return {
        "success": True,
        "device": device.name,
        "status": status,
        "last_seen": device.last_seen
    }