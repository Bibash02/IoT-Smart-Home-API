from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    class RoomType(models.TextChoices):
        LIVING_ROOM = "LIVING_ROOM", "Living Room"
        BEDROOM = "BEDROOM", "Bedroom"
        KITCHEN = "KITCHEN", "Kitchen"
        BATHROOM = "BATHROOM", "Bathroom"
        GARAGE = "GARAGE", "Garage"
        OFFICE = "OFFICE", "Office"
        OTHER = "OTHER", "Other"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=50)
    room_type = models.CharField(max_length=30, choices=RoomType.choices, default=RoomType.OTHER)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
