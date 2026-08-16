from django.urls import path
from .views import DeviceCommandAPIView

urlpatterns = [
    path('device/<device_id/command', DeviceCommandAPIView.as_view(), name='device-command'),
]