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

class NotificationMarkReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(id = pk, user = request.user)
        except Notification.DoesNotExist:
            return Response({
                "detail": "Notification not found."
            }, status=404)
        

        notification.is_read = True
        notification.save(update_fields=['is_read'])

        return Response({
            "message": "Notification marked as read.",
            "notification_id": notification.id,
            "is_read": notification.is_read
        }, status=200)

class NotificationMarkAllReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        updated_count = Notification.objects.filter(user = request.user, is_read = False).update(is_read = True)

        return Response({
            "message": "All notifications marked as read.",
            "updated_count": updated_count
        }, status=200)

class UnreadNotificationcountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(user = request.user, is_read = False).count()

        return Response({
            'unread_count': count
        })

class MarkNotificationReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            notification = Notification.objects.get(id = pk, user = request.user)
        except Notification.DoesNotExist:
            return Response({
                "detail": "Notification not found."
            }, status=404)

        notification.is_read = True

        notification.save(
            update_fields=['is_read']
        )

        return Response({
            "success": True,
            "message":  "Notification marked as read."
        })

class MarkAllNotificationReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        updated = Notification.objects.filter(
            user = request.user, is_read = False
        ).update(is_read = True)

        return Response({
            "success": True,
            "updated": updated,
            "message": "All notifications marked as read."
        })