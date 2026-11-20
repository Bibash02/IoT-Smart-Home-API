from django.urls import path
from .views import *

urlpatterns = [
    path('sensor/', SensorListCreateAPIView.as_view(), name='sensor-list-create'),
    path('sensor/<int:pk>', SensorRetrieveUpdateDestroyAPIView.as_view(), name='sensor-detail'),
    # sensor readings
    path('sensor/readings/', SensorReadingCreateAPIView.as_view(), name='sensor-reading-create'),
    path('sensor/<int:pk>/readings/', SensorReadingHistoryAPIView.as_view(), name='sensor-reading-history'),
    path('sensor/<int:pk>/latest', SensorLatestReadingAPIView.as_view(), name='sensor-latest-reading'),
]