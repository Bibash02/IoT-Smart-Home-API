from django.db import models
from django.contrib.auth.models import User
from devices.models import Device
from sensors.models import Sensor

# Create your models here.
class AutomationRule(models.Model):
    class ConditionOperator(models.TextChoices):
        GREATER_THEN = ">", "Greater Then"
        GREATER_LESS = "<", "Greater Less"
        EQUAL = "=", "Equal"
        GREATER_EQUAL = ">=", "Greater or Equal"
        LESS_EQUAL = "<=", "Less or Equal"

    class Action(models.TextChoices):
        TURN_ON = "TURN_ON", "Turn On"
        TURN_OFF = "TURN_OFF", "Turn Off"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='automation_rules')
    name = models.CharField(max_length=50)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='automation_rules')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='automation_rules')
    operator = models.CharField(max_length=5, choices=ConditionOperator.choices)
    threshold = models.FloatField()
    action = models.CharField(max_length=20, choices=Action.choices)
    last_triggered_at = models.DateTimeField(null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AutomationExecution(models.Model):
    class ExecutionStatus(models.TextChoices):
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
        SKIPPED = "SKIPPED", "Skipped"

    rule = models.ForeignKey(AutomationRule, on_delete=models.CASCADE, related_name='executions')
    sensor_value = models.FloatField()
    action = models.CharField(max_length=20)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='automation_executions', null=True, blank=True)
    status = models.CharField(max_length=20, choices=ExecutionStatus.choices)
    message = models.TextField(blank=True)
    command = models.ForeignKey('devices.DeviceCommand', on_delete=models.SET_NULL, null=True, blank=True, related_name='automation_executions')
    success = models.BooleanField(default=True)
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rule.name} - {self.executed_at}"