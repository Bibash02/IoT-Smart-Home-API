from django.urls import path
from .views import DeviceCommandAPIView, DeviceAuthenticationAPIView, DeviceHeartbeatAPIView, DeviceCommandCreateAPIView, DeviceCommandListAPIView, DeviceCommandHistoryAPIView

urlpatterns = [
    path('device/<device_id>/command', DeviceCommandAPIView.as_view(), name='device-command'),
    path('device/auth/', DeviceAuthenticationAPIView.as_view(), name='device-auth'),
    path('device/heartbeat/', DeviceHeartbeatAPIView.as_view(), name='device-heartbeat'),
    path('device/commands/', DeviceCommandCreateAPIView.as_view(), name='command-create'),
    path('device/command/history', DeviceCommandListAPIView.as_view(), name='command-list'),
    path('device/<int:pk>/commands/', DeviceCommandHistoryAPIView.as_view(), name='device-command-history'),
]