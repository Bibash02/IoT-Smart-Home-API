from rest_framework import serializers
from .models import Device, DeviceCommand, DeviceToken

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

        def validate_room(self, room):
            request = self.context["request"]

            if room.user != request.user:
                raise serializers.ValidationError(
                    "You cannot add a device to another user's room."
                )
            return room

class DeviceAuthSerializer(serializers.Serializer):
    device_uid = serializers.CharField(max_length = 100)
    device_secret = serializers.CharField(max_length = 128, write_only = True)

class DeviceHeartbeatSerializer(serializers.Serializer):
    device_uid = serializers.CharField(max_length = 100)
    device_secret = serializers.CharField(max_length = 128, write_only = True)

class DeviceCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceCommand
        fields = [
            'id',
            'device',
            'command',
            'value',
            'status',
            'response',
            'created_at',
            'executed_at'
        ]
        read_only_fields = [
            'id',
            'status',
            'response',
            'created_at',
            'executed_at'
        ]

        def validate_device(self, device):
            request = self.context['request']

            if device.user != request.user:
                raise serializers.ValidationError(
                    "This device does not belong to you."
                )

            return device

class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = [
            'device',
            'token',
            'is_active',
            'created_at',
            'last_used_at'
        ]
        read_only_fields = [
            'token',
            'created_at',
            'last_used_at'
        ]