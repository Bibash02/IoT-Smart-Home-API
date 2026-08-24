from .models import AutomationRule
from devices.models import DeviceCommand
from notifications.services import create_notification

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
    condition_met = check_condition(rule.operator, sensor_value, rule.threshold)

    if not condition_met:
        return {
            "executed": False,
            "reason": "Conditon not satisfied."
        }

    # execute device action
    command = DeviceCommand.objects.create(
        device = rule.device,
        command = rule.action,
        status = "PENDING"
    )

    # create notification
    create_notification(
        user = rule.user, 
        title="Automation executed.",
        message=(
            f"Automation '{rule.name}' executed.",
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
        "command_id": command.id
    }