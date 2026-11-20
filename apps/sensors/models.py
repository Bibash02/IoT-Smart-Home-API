from django.db import models
from apps.devices.models import Device

# Create your models here.
class Sensor(models.Model):
    class SensorType(models.TextChoices):
        TEMPRATURE = "TEMPRATURE", "Temprature"
        HUMIDITY = "HUMIDITY", "Humidity"
        MOTION = "MOTION", "Motion"
        GAS = "GAS", "Gas"
        SMOKE = "SMOKE", "Smoke"
        LIGHT = "LIGHT", "Light"
        SOUND = "SOUND", "Sound"
        WATER = "WATER", "Water"
        OTHER = "OTHER", "Other"

    sensor_uid = models.CharField(max_length=100, unique=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='sensors')
    name = models.CharField(max_length=50)
    sensor_type = models.CharField(max_length=30, choices=SensorType.choices, default=SensorType.OTHER)
    unit = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.sensor_type}"

class SensorReading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    value = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.sensor.name} - {self.value}"