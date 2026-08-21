from django.urls import path
from .views import DeviceCommandAPIView, DeviceAuthenticationAPIView, DeviceHeartbeatAPIView

urlpatterns = [
    path('device/<device_id>/command', DeviceCommandAPIView.as_view(), name='device-command'),
    path('device/auth/', DeviceAuthenticationAPIView.as_view(), name='device-auth'),
    path('device/heartbeat/', DeviceHeartbeatAPIView.as_view(), name='device-heartbeat'),
]