from sensors.models import Sensor, SensorReading
from automation.models import AutomationRule
from automation.services import execute_automation

def process_sensor_data(device_uid, sensor_uid, value):
    try:
        sensor = Sensor.objects.select_related('device').get(sensor_uid = sensor_uid)
    except Sensor.DoesNotExist:
        return {
            "success": False,
            "reason": "Sensor does not belong to this device."
        }

    # create sensor reading
    reading = SensorReading.objects.create(sensor = sensor, value = value)

    # find automation rules
    rules = AutomationRule.objects.filter(sensor = sensor, is_enabled = True).select_related('device', 'user')

    automation_results = []

    for rule in rules:
        result = execute_automation(rule = rule, sensor_value=value)
        automation_results.append(result)

    return {
        "success": True,
        "sensor": sensor.name,
        "value": value,
        "reading_id": reading.id,
        "automation": automation_results
    }