

def command_topic(device_uid):
    return f"smarthome/devices/{device_uid}/command"

def sensor_topic(device_uid):
    return f"smarthome/devices/{device_uid}/sensor"

def status_topic(device_uid):
    return f"smarthome/devices/{device_uid}/status"

def response_topic(device_uid):
    return f"smarthome/devices/{device_uid}/response"

def heartbeat_topic(device_uid):
    return (f"smarthome/devices/"
    f"{device_uid}/hearbeat")

def energy_topic(device_uid):
    return (
        f"smarthome/devices/"
        f"{device_uid}/energy"
    )