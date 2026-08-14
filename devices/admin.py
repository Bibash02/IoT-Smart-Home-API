from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'name', 'device_uid', 'device_type', 'status', 'is_online', 'ip_address', 'flameware_version', 'last_seen', 'created_at', 'updated_at']
    search_fields = ['user', 'name', 'device_uid', 'room']
    list_filter = ['device_uid', 'room', 'device_type']

@admin.register(DeviceCommand)
class DeviceCommandAdmin(admin.ModelAdmin):
    list_display = ['device', 'command', 'value', 'response', 'created_at', 'executed_at']
    list_filter = ['device', 'value']
    search_fields = ['device', 'command']