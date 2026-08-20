from django.urls import path
from .views import DeviceCommandAPIView, DeviceAuthenticationAPIView

urlpatterns = [
    path('device/<device_id>/command', DeviceCommandAPIView.as_view(), name='device-command'),
    path('device/auth/', DeviceAuthenticationAPIView.as_view(), name='device-auth'),
]