from django.contrib import admin
from .models import AutomationRule

# Register your models here.
@admin.register(AutomationRule)
class AutomationRuleAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'sensor', 'device', 'operator', 'threshold', 'action', 'is_enabled', 'created_at', 'updated_at']
    list_filter = ['device', 'is_enabled', 'action']
    search_fields = ['user', 'name', 'device']