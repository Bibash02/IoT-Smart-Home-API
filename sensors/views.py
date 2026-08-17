from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import SensorReading, Sensor
from .serializers import SensorReadingSerializer, SensorSerializer

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