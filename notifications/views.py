from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .models import Notification
from .serializers import NotificationSerializer

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user = self.request.user).order_by("-created_at")

class NotificationDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user = self.request.user)
