from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import SensorReading, Sensor
from .serializers import SensorReadingSerializer, SensorSerializer

from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class SensorListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Sensor.objects.filter(device__user = self.request.user).select_related("device").order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save()

class SensorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Sensor.objects.filter(device__user = self.request.user)

class SensorReadingCreateAPIView(generics.CreateAPIView):
    serializer_class = SensorReadingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class SensorReadingHistoryAPIView(generics.ListAPIView):
    serializer_class = SensorReadingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sensor_id = self.kwargs["pk"]
        return SensorReading.objects.filter(
            sensor_id = sensor_id, sensor__device__user = self.request.user
            ).order_by("-recorded_at")


class SensorLatestReadingAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        sensor = Sensor.objects.filter(id = pk, device__user = request.user).first()

        if not sensor:
            return Response({
                "detail": "Sensor not found."
            }, status=400)

        reading = SensorReading.objects.filter(sensor = sensor).order_by("-recorded_at").first()

        if not reading:
            return Response({
                "detail": "No readings available for this sensor."
            }, status=404)

        return Response({
            "sensor": sensor.name,
            "sensor_type": sensor.sensor_type,
            "unit": sensor.unit,
            "value": reading.value,
            "recorded_at": reading.recorded_at,
        })
