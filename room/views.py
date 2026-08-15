from django.shortcuts import render
from .serializers import RoomSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Room

# Create your views here.
class RoomListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Room.objects.filter(user = self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class RoomRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Room.objects.filter(user = self.request.user)

