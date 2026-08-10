from django.db import models
from django.contrib.auth.models import User
from room.models import Room

# Create your models here.
class Device(models.Model):
    class DeviceType(models.TextChoices):
        LIGHT = "LiGHT", "Light"
        FAN = "FAN", "Fan"
        AC = "AC", "Ac"
        TV = "TV", "Tv"
        LOCK = "LOCK", "Lock"
        CAMERA = "CAMERA", "Camera"
        SENSOR = "SENSOR", "Sensor"
        SWITCH = "SWITCH", "Switch"
        OTHER = "OTHER", "Other"

    class DeviceStatus(models.TextChoices):
        ON = "ON", "On"
        OF = "OF", "Of"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=50)
    device_uid = models.CharField(max_length=50, unique=True)
    device_type = models.CharField(max_length=30, choices=DeviceType.choices, default=DeviceType.OTHER)
    status = models.CharField(max_length=10, choices=DeviceStatus.choices, default=DeviceStatus.OF)
    is_online = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    flameware_version = models.CharField(max_length=50, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
