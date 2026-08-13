from django.db import models
from devices.models import Device

# Create your models here.
class EnergyReading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='energy_readings')
    voltage = models.FloatField(null=True, blank=True)
    current = models.FloatField(null=True, blank=True)
    power = models.FloatField(null=True, blank=True)
    energy_consumed = models.FloatField(default=0)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.device.name} - {self.power} W"