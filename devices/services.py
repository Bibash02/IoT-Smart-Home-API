from django.utils import timezone
from .models import Device, DeviceCommand

def execute_device_command(device, command_type, value=None):
    # check device online
    if not device.is_online:
        raise ValueError("Device is offline.")

    # validate command
    valid_commands = DeviceCommand.CommandType.values

    if command_type not in valid_commands:
        raise ValueError(
            f"Invalid command: {command_type}"
        )

    # create command
    command = DeviceCommand.objects.create(
        device = device,
        command = command_type,
        value = value,
        status = DeviceCommand.CommandStatus.PENDING
    )

    try:
        # power
        if command_type == DeviceCommand.CommandType.POWER:
            if value not in ["ON", "OFF"]:
                raise ValueError("POWER value must be ON or OF.")

            if value == "ON":
                device.status = Device.DeviceStatus.ON
            else:
                device.status = Device.DeviceStatus.OF

            device.save(
                update_fields = ['status', 'updated_at']
            )

        # light
        elif command_type == DeviceCommand.CommandType.LIGHT:
            if device.device_type != Device.DeviceType.LIGHT:
                raise ValueError("LIGHT command can only be used with a light.")

            if value is None:
                raise ValueError("Light value is required.")

            if value == "ON":
                device.status = Device.DeviceStatus.ON
                device.save(update_fields = ["status", "updated_at"])

            elif value == "Of":
                device.status = Device.DeviceStatus.OF
                device.save(update_fields = ["status", "updated_at"])

        # fan speed
        elif command_type == DeviceCommand.CommandType.SPEED:
            if device.device_type != Device.DeviceType.FAN:
                raise ValueError("SPEED command can only be used with a fan.")

            if value is None:
                raise ValueError(
                    "Fan speed is required."
                )

            try:
                speed = int(value)
            except ValueError:
                raise ValueError("Fan speed must be a number.")

            if speed < 0 or speed > 5:
                raise ValueError("FAN speed must be between 0 and 5.")

        # temprature
        elif command_type == DeviceCommand.CommandType.TEMPRATURE:
            if device.device_type != Device.DeviceType.AC:
                raise ValueError("TEMPRATURE command can only be used with AC.")

            if value is None:
                raise ValueError("Temprature is required.")

            try:
                temprature = int(value)
            except ValueError:
                raise ValueError("Temprature must be a number.")

            if temprature < 16 or temprature > 30:
                raise ValueError("Temprature must be between 16 and 30C.")

        # Lock
        elif command_type == DeviceCommand.CommandType.LOCK:
            if device.device_type != Device.DeviceType.LOCK:
                raise ValueError("LOCK command can only be used with a lock.")

        # unlock
        elif command_type == DeviceCommand.CommandType.UNLOCK:
            if device.device_type != Device.DeviceType.LOCK:
                raise ValueError("UNLOCK command can only be used with a lock.")

        command.status = DeviceCommand.CommandStatus.SUCCESS
        command.response = "Command executed successfully."
        command.executed_at = timezone.now()
        command.save(
            update_fields = ['status', 'response', 'executed_at']
        )

        return command

    # command failed
    except Exception as error:
        command.status = DeviceCommand.CommandStatus.FAILED
        command.response = str(error)
        command.executed_at = timezone.now()
        command.save(
            update_fields = ['status', 'response', 'executed_at']
        )
        raise
    