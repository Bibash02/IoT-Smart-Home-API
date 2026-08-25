from django.db.models.signals import post_save
from django.dispatch import receiver

from sensors.models import SensorReading
from .services import process_sensor_reading

@receiver(post_save, sender=SensorReading)
def sensor_reading_created(sender, instance, created, **kwargs):
    if not created:
        return

    process_sensor_reading(sensor=instance.sensor, value=instance.value)