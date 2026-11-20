from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
    class NotificationType(models.TextChoices):
        SECURITY = "SECURITY", "Security"
        SENSOR = "SENSOR", "Sensor"
        DEVICE = "DEVICE", "Device"
        AUTOMATION = "AUTOMATION", "Automation"
        ENERGY = "ENERGY", "Energy"
        SYSTEM = "SYSTEM", "System"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=50)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NotificationType.choices)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
