from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .models import EnergyReading
from .serializers import EnergyReadingSerializer

from rest_framework.response import Response
from rest_framework import status

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
            }, status=404)

        reading = EnergyReading.objects.filter(device = device).first()

        if not reading:
            return Response({
                "detail": "No energy reading available."
            }, status=404)

        return Response({
            "device": device.name,
            "voltage": reading.voltage,
            "current": reading.current,
            "power": reading.power,
            "energy_consumed": reading.energy_consumed,
            "recorded_at": reading.recorded_at
        })
    