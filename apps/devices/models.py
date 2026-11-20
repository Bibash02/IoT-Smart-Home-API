from django.db import models
from django.contrib.auth.models import User
from apps.room.models import Room
import secrets

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
    device_secret = models.CharField(max_length=128, unique=True, editable=False)
    device_type = models.CharField(max_length=30, choices=DeviceType.choices, default=DeviceType.OTHER)
    status = models.CharField(max_length=10, choices=DeviceStatus.choices, default=DeviceStatus.OF)
    is_online = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    flameware_version = models.CharField(max_length=50, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.device_secret:
            self.device_secret = secrets.token_urlsafe(48)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class DeviceCommand(models.Model):
    class CommandType(models.TextChoices):
        POWER = "POWER", "Power"
        LIGHT = "LIGHT", "Light"
        SPEED = "SPEED", "Speed"
        TEMPRATURE = "TEMPRATURE", "Temprature"
        LOCK = "LOCK", "Lock"
        UNLOCK = "UNLOCK", "Unlock"

    class CommandStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSING = "PROCESSING", "Processing"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='commands')
    command = models.CharField(max_length=30, choices=CommandType.choices)
    value = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=CommandStatus.choices, default=CommandStatus.PENDING)
    response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null = True, blank=True)

    def __str__(self):
        return f"{self.device.name} - {self.command}"

class DeviceToken(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name='token')
    token = models.CharField(max_length=128, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(64)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.device.name} Token"
    