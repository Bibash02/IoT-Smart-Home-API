from rest_framework import serializers
from .models import AutomationRule, AutomationExecution

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

class AutomationExecutionSerializer(serializers.ModelSerializer):
    rule_name = serializers.CharField(source = "rule.name", read_only = True)
    device_name = serializers.CharField(source="rule.name", read_only = True)

    class Meta:
        model = AutomationExecution
        fields = [
            'id',
            'rule',
            'rule_name',
            'sensor_value',
            'action',
            'device',
            'device_name',
            'status',
            'message',
            'command',
            'executed_at'
        ]


        