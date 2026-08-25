from .models import AutomationRule
from devices.models import DeviceCommand
from notifications.services import create_notification
from devices.services import execute_device_command

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

    if not condition_met:
        return {
            "executed": False,
            "reason": "Condition not satisfied."
        }

    # Convert automation action
    # into device command
    if rule.action == "TURN_ON":

        command_type = "POWER"
        value = "ON"

    elif rule.action == "TURN_OFF":

        command_type = "POWER"
        value = "OFF"

    else:

        return {
            "executed": False,
            "reason": "Unsupported automation action."
        }

    # Execute device command
    try:

        command = execute_device_command(
            device=rule.device,
            command_type=command_type,
            value=value
        )

    except ValueError as error:

        return {
            "executed": False,
            "reason": str(error)
        }

    # Create notification
    create_notification(
        user=rule.user,
        title="Automation Executed",
        message=(
            f"Automation '{rule.name}' executed. "
            f"Device '{rule.device.name}' "
            f"action: {rule.action}."
        ),
        notification_type="AUTOMATION"
    )

    return {
        "executed": True,
        "rule": rule.name,
        "device": rule.device.name,
        "action": rule.action,
        "command": command.command,
        "value": command.value,
        "status": command.status,
        "command_id": command.id
    }

def process_sensor_reading(sensor, value):
    rules = AutomationRule.objects.filter(sensor = sensor, is_enabled = True).select_related('device', 'user')

    results = []

    for rule in rules:
        result = execute_automation(rule, value)
        results.append(result)

    return results