from rest_framework import serializers
from .models import Sensor, SensorReading
from devices.models import Device

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'device', 'name', 'sensor_type', 'unit', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

        def validate_device(self, device):
            request = self.context["request"]
            if device.user != request.user:
                raise serializers.ValidationError(
                    "You cannot add a sensor to another user's device."
                )
            return device



class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = ['id', 'sensor', 'value', 'recorded_at']
        read_only_fields = ['id', 'recorded_at']

        def validate_sensor(self, sensor):
            request = self.context["request"]

            if sensor.device.user != request.user:
                raise serializers.ValidationError(
                    "You cannot add readings to another user's sensor."
                )
            return sensor
        