from django.utils import timezone
from .models import EnergyReading
from django.db.models import Sum
from notifications.services import create_notification

def create_energy_reading(device, voltage, current, power):
    previous_reading = (EnergyReading.objects.filter(device = device).order_by('-recorded_at').first())

    energy_consumed = 0

    if previous_reading:
        time_difference = (
            timezone.now()
            - previous_reading.recorded_at
        )

        hours = (
            time_difference.total_seconds() / 3600
        )

        energy_consumed = power * hours

    reading = EnergyReading.objects.create(
        device = device,
        voltage = voltage,
        current = current,
        power = power,
        energy_consumed = energy_consumed
    )

    return reading

def get_daily_energy(device, data = None):
    if data is None:
        data = timezone.localdate()

    total_wh = (
        EnergyReading.objects
        .filter(
            device=device,
        )
        .aggregate(
            total=Sum("energy_consumed")
        )
        ["total"]
        or 0
    )

    total_kwh = total_wh / 1000

    return {
        "device": device.name,
        "energy_wh": round(total_wh, 3),
        "energy_kwh": round(total_kwh, 3)
    }

def get_monthly_energy(device, year, month):
    total_wh = (
        EnergyReading.objects.filter(
            device = device,
            recorded_at__year = year,
            recorded_at__month = month
        )
        .aggregate(total = Sum("energy_consumed"))['total'] or 0
    )

    return {
        'device': device.name,
        'year': year,
        'month': month,
        'energy_wh': round(total_wh, 3),
        'energy_kwh': round(total_wh / 1000, 3)
    }

def check_energy_list(device, energy_kwh, limit_kwh = 5):
    if energy_kwh <= limit_kwh:
        return False

    create_notification(
        user = device.user,
        title = "High Energy Usage",
        message=(
            f"Device {device.name}"
            f"has consumed "
            f"{energy_kwh:.2f} kwh today."
        ),
        notification_type="ENERGY"
    )
    return True
