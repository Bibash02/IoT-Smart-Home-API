from .models import AutomationRule, AutomationExecution
from apps.devices.models import DeviceCommand
from apps.notifications.services import create_notification
from apps.devices.services import execute_device_command
from django.utils import timezone

def check_condition(operator, sensor_value, threshold):
    if operator == ">":
        return sensor_value > threshold
    elif operator == "<":
        return sensor_value < threshold
    elif operator == "=":
        return sensor_value == threshold
    elif operator == ">=":
        return sensor_value >= threshold
    elif operator == "<=":
        return sensor_value <= threshold

    return False

def execute_automation(rule, sensor_value):
    condition_met = check_condition(
        rule.operator,
        sensor_value,
        rule.threshold
    )

    previous_condition = rule.last_condition_met

    # save current condition state
    rule.last_condition_met = condition_met

    # condition is false
    if not condition_met:
        rule.save(
            update_fields = [
                'last_condition_met',
                'updated_at'
            ]
        )

        AutomationExecution.objects.create(
            rule = rule,
            sensor_value = sensor_value,
            action = rule.action,
            device = rule.device,
            status = AutomationExecution.ExecutionStatus.SKIPPED,
            message = "Condition not satisfied."
        )

        return {
            'executed': False,
            'reason': "Condition not satisfied."
        }

    # condition was already true
    if previous_condition is True:
        rule.save(
            update_fields = [
                'last_condition_met',
                'updated_at'
            ]
        )

        AutomationExecution.objects.create(
            rule=rule,
            sensor_value=sensor_value,
            action=rule.action,
            device=rule.device,
            status=AutomationExecution.ExecutionStatus.SKIPPED,
            message="Condition already satisfied."
        )

        return {
            'executed': False,
            'reason': 'Condition already satisfied.'
        }

    # condition changed false -> true
    if rule.action == "TURN_ON":
        command_type = DeviceCommand.CommandType.POWER
        value = "ON"
    elif rule.action == "TURN_OFF":
        command_type = DeviceCommand.CommandType.POWER
        value = "OFF"
    else:
        AutomationExecution.objects.create(
            rule = rule,
            sensor_value = sensor_value,
            action = rule.action,
            device = rule.device,
            status = AutomationExecution.ExecutionStatus.FAILED,
            message = "Unsupported automation action."
        )

        return {
            'executed': False,
            'reason': 'Unsupported automation action.'
        }

    # execute device command
    try:
        command = execute_device_command(
            device=rule.device,
            command_type=command_type,
            value=value
        )
    except ValueError as error:
        AutomationExecution.objects.create(
            rule = rule,
            sensor_value = sensor_value,
            action = rule.action,
            device = rule.device,
            status = AutomationExecution.ExecutionStatus.FAILED,
            message = str(error)
        )

        return {
            'executed': False,
            'reason': str(error)
        }

    # updated automation
    rule.last_triggered_at = timezone.now()

    rule.save(
        update_fields = [
            'last_condition_met',
            'last_triggered_at',
            'updated_at'
        ]   
    )

    # save execution history
    execution = AutomationExecution.objects.create(
        rule = rule,
        sensor_value = sensor_value,
        action = rule.action,
        device = rule.device,
        command = command,
        status = AutomationExecution.ExecutionStatus.SUCCESS,
        message = "Automation executed successfully."
    )

    # create notification
    create_notification(
        user=rule.user,
        title="Automation executed.",
        message=(
            f"Automation '{rule.name}' executed. "
            f"Device '{rule.device.name}' "
            f"action: {rule.action}."
        ),
        notification_type="AUTOMATION"
    )

    return {
        'executed': True,
        'rule': rule.name,
        'device': rule.device.name,
        'action': rule.action,
        'command': command.command,
        'value': command.value,
        'status': command.status,
        'command_id': command.id
    }

def process_sensor_reading(sensor, value):
    rules = AutomationRule.objects.filter(sensor = sensor, is_enabled = True).select_related('device', 'user')

    results = []

    for rule in rules:
        result = execute_automation(rule, value)
        results.append(result)

    return results