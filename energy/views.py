from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .models import EnergyReading
from .serializers import EnergyReadingSerializer

from rest_framework.response import Response
from rest_framework import status

from django.db.models import Sum
from django.utils import timezone

from django.db.models.functions import TruncMonth

# Create your views here.
class EnergyReadingListCreatAPIView(generics.ListCreateAPIView):
    serializer_class = EnergyReadingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EnergyReading.objects.filter(device__user = self.request.user).select_related('device')

    def perform_create(self, serializer):
        serializer.save()

class EnergyReadingDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = EnergyReadingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EnergyReading.objects.filter(device__user = self.request.user)

class DeviceEnergyHistoryAPIView(generics.ListAPIView):
    serializer_class = EnergyReadingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        device_id = self.kwargs['pk']

        return EnergyReading.objects.filter(device_id = device_id, device__user = self.request.user).order_by('-recorded_at')

class DeviceLatestEnergyAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        device = request.user.device.filter(id = pk).first()

        if not device:
            return Response({
                "detail": "Device not found."
            }, status=status.HTTP_404_NOT_FOUND)

        reading = EnergyReading.objects.filter(device = device).first()

        if not reading:
            return Response({
                "detail": "No energy reading available."
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "device": device.name,
            "voltage": reading.voltage,
            "current": reading.current,
            "power": reading.power,
            "energy_consumed": reading.energy_consumed,
            "recorded_at": reading.recorded_at
        })

class DailyEnergyAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()

        total_energy = EnergyReading.objects.filter(
            device__user = self.request.user, recorded_at__date = today
            ).aggregate(
                total = Sum('energy_consumed')
            )['total'] or 0

        return Response({
            "date": today,
            'total_energy_consumed': round(total_energy, 3), 'unit': 'kwh'
        })

class MonthlyEnergyAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        monthly_data = (
            EnergyReading.objects.filter(
                device__user = request.user
                ).annotate(
                    month = TruncMonth('recorded_at')
                    )
                    .values('month')
                    .annotate(total_energy = Sum('energy_consumed')).order_by('-month')
        )

        data = []

        for item in monthly_data:
            data.append({
                'month': item['month'],
                'total_energy_consumed': round(
                    item['total_energy'] or 0,
                    3
                ),
                'unit': 'kwh'
            }
        )

        return Response(data)

class DeviceEnergySummeryAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def ge(self, request):
        device_data = (
            EnergyReading.objects.filter(device__user = request.user)
            .values('device', 'device__name')
            .annotate(total_energy = Sum('energy_consumed'))
            .order_by('-total_energy')
        )

        data = []

        for item in device_data:
            data.append({
                'device_id': item['device'],
                'device': item['device__name'],
                'total_energy_consumed': round(
                    item['total_energy'] or 0,
                    3
                ),
                'unit': 'kwh'
            }
        )

        return Response(data)


