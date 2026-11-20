from django.utils import timezone
from datetime import timedelta
from .models import EnergyReading
from django.db.models import Sum, Avg, Max
from apps.notifications.services import create_notification

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

def get_energy_summary(user):
    # Return overall energy statistics for the logged-in user.

    today = timezone.localdate()

    # today's energy
    today_energy = (
        EnergyReading.objects.filter(
            device__user = user,
            recorded_at__date = today
        )
        .aggregate(
            total = Sum("energy_consumed")
        )['total'] or 0
    )

    # current month
    month_energy = (
        EnergyReading.objects.filter(
            device__user = user,
            recorded_at__year = today.year,
            recorded_at__month = today.month
        )
        .aggregate(
            total = Sum("energy_consumed")
        )['total'] or 0
    )

    # total energy
    total_energy = (
        EnergyReading.objects.filter(
            device__user = user
        )
        .aggregate(
            total = Sum("energy_consumed")
        )["total"] or 0
    )

    # Highest consuming device
    device_usage = (
        EnergyReading.objects.filter(
            device__user = user
        )
        .values(
            "device__id", "device__name"
        )
        .annotate(
            total_energy = Sum("energy_consumed")
        )
        .order_by('-total_energy').first()
    )

    highest_device = None

    if device_usage:
        highest_device = {
            "id": device_usage['device__id'],
            "name": device_usage['device__name'],
            "energy_kwh": round(
                device_usage['total_energy'] / 1000, 3
            )
        }

    return {
        "today": {
            "energy_wh": round(total_energy, 3),
            "energy_kwh": round(total_energy / 1000, 3)
        },
        "this_month": {
            "energy_wh": round(month_energy, 3),
            "energy_kwh": round(month_energy / 1000, 3)
        },
        "total": {
            "energy_wh": round(total_energy, 3),
            "energy_kwh": round(total_energy / 3000, 3)
        },
        "highest_consuming_device": highest_device
    }

def get_today_device_usage(user):
    today = timezone.localdate()

    usage = (
        EnergyReading.objects.filter(
            device__user = user,
            recorded_at__date = today
        )
        .values(
            "device__id", "device__name"
        )
        .annotate(
            energy = Sum('energy_consumed'),
            average_power = Avg('power'),
            maximum_power = Max('power')
        )
        .order_by(
            '-energy'
        )
    )

    result = []

    for item in usage:
        result.append({
            "device_id": item["device__id"],
            "device_name": item["device__name"],
            "energy_wh": round(item['energy'] or 0, 3),
            "energy_kwh": round((item['energy'] or 0) / 1000, 3),
            "average_power": round(item['averge_power'] or 0, 2),
            "maximum_power": round(item['maximum_power'] or 0, 2)
        })

    return result

def get_weekly_energy(user):
    today = timezone.localdate()

    start_date = (today - timedelta(days = 6))

    readings = (
        EnergyReading.objects.filter(
            device__user = user,
            recorded_at__date__gte = start_date,
            recorded_at__date__lte = today
        )
        .values('recorded_at__date')
        .annotate(energy = Sum('energy_consumed'))
        .order_by('recorded_at__date')
    )

    result = []

    for item in readings:
        energy = item['energy'] or 0

        result.append({
            'date': item['recorded_at__date'],
            'energy_wh': round(energy, 3),
            'energy_kwh': round(energy / 1000, 3)
        })

    return result

