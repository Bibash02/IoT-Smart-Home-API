from django.contrib import admin
from .models import Sensor, SensorReading

# Register your models here.
@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['device', 'name', 'sensor_type', 'unit', 'is_active', 'created_at']
    list_filter = ['sensor_type', 'is_active', 'unit']
    search_fields = ['name', 'is_active', 'device']