from rest_framework import serializers
from .models import EnergyReading

class EnergyReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyReading
        fields = ['id', 'device', 'voltage', 'current', 'power', 'energy_consumed', 'recorded_at']
        read_only_fields = ['id', 'recorded_at']

        def validate_device(self, device):
            request = self.context['request']

            if device.user != request.user:
                raise serializers.ValidationError(
                    "You cannot add energy data to another user's device."
                )
            return device
        