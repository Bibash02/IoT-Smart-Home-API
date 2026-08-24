from rest_framework import serializers
from .models import AutomationRule

class AutomationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationRule
        fields = ['id', 'name', 'sensor', 'device', 'operator', 'threshold', 'action', 'is_enabled', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

        def validate(self, data):
            request = self.context['request']

            sensor = data.get('sensor')
            device = data.get('device')

            # Make sure sensor belongs to current user
            if sensor.user != request.user:
                raise serializers.ValidationError({
                    "sensor": "This sensor does not belongs to you."
                })

            return data
        