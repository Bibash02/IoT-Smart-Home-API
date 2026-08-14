from django.contrib import admin
from .models import EnergyReading

# Register your models here.
@admin.register(EnergyReading)
class EnergyReadingAdmin(admin.ModelAdmin):
    list_display = ['device', 'voltage', 'current', 'power', 'energy_consumed', 'recorded_at']
    list_filter = ['device', 'voltage']
    search_fields = ['device']