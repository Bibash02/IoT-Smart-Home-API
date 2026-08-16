from rest_framework import serializers
from .models import Device, DeviceCommand

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'id',
            'room',
            'name',
            'device_uid',
            'device_type',
            'status',
            'is_online',
            'ip_address',
            'flameware_version',
            'last_seen',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'status',
            'is_online',
            'last_seen',
            'created_at',
            'updated_at',
        ]

class DeviceCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceCommand
        fields = [
            'id',
            'device',
            'command',
            'value',
            'response',
            'created_at',
            'executed_at'
        ]
        read_only_fields = [
            'id',
            'status',
            'created_at',
            'executed_at'
        ]