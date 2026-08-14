from django.contrib import admin
from .models import Room

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'room_type', 'description', 'created_at', 'updated_at']
    list_filter = ['room_type', 'name']
    search_fields = ['name', 'room_type']