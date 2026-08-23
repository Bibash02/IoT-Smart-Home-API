from django.urls import path
from .views import EnergyReadingListCreatAPIView, EnergyReadingDetailAPIView, DeviceEnergyHistoryAPIView, DeviceEnergySummeryAPIView, DeviceLatestEnergyAPIView, MonthlyEnergyAPIView, DailyEnergyAPIView

urlpatterns = [
    path('energy/', EnergyReadingListCreatAPIView.as_view(), name='energy-list-create'),
    path('energy/detail/', EnergyReadingDetailAPIView.as_view(), name='energy-detail'),
    path('energy/device/history/', DeviceEnergyHistoryAPIView.as_view(), name='device-energy-history'),
    path('energy/device/summery/', DeviceEnergySummeryAPIView.as_view(), name='device-energy-summery'),
    path('energy/device/latest/', DeviceLatestEnergyAPIView.as_view(), name='device-energy-latest'),
    path('energy/daily/', DailyEnergyAPIView.as_view(), name='daily-energy'),
    path('energy/monthly/', MonthlyEnergyAPIView.as_view(), name='monthly-energy'),
]