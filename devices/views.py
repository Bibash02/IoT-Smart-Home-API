from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from rest_framework import status

from .models import DeviceCommand, Device
from .serializers import DeviceSerializer, DeviceCommandSerializer, DeviceAuthSerializer, DeviceHeartbeatSerializer
from .services import execute_device_command
from datetime import timezone

# Create your views here.
class DeviceCommandAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, device_id):
        # get device
        try:
            device = Device.objects.get(id = device_id, user = request.user)
        except Device.DoesNotExist:
            return Response({
                "error": "Device not found."
            }, status=404)

        # get data
        command_type = request.data.get("command")
        value = request.data.get("value")

        # validation
        if not command_type:
            return Response({
                "error": "Command is required"
            }, status=400)

        # execute command
        try:
            command = execute_device_command(device = device, command_type = command_type, value = value)
        except ValueError as error:
            return Response({
                "error": str(error)
            }, status=400)

        # response
        serializer = DeviceCommandSerializer(command)

        return Response({
            "message": "Command executed successfully.",
            "command": serializer.data
        }, status=200)

class DeviceAuthenticationAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = DeviceAuthSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        device_uid = serializer.validated_data["device_uid"]
        device_secret = serializer.validated_data["device_secret"]

        try:
            device = Device.objects.get(device_uid = device_uid)
        except Device.DoesNotExist:
            return Response({
                "detail": "Invalid device credentials."
            }, status=401)

        if device.device_secret != device_secret:
            return Response({
                "detail": "Invalid device credentials."
            }, status=401)

        return Response({
            "message": "Device authenticated successfully.",
            "device_id": device.id,
            "device_uid": device.device_uid,
            "device_type": device.device_type,
            "user_id": device.user_id
        }, status=200)

class DeviceHeartbeatAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = DeviceHeartbeatSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        device_uid = serializer.validated_data["device_uid"]
        device_secret = serializer.validated_data["device_secret"]

        try:
            device = Device.objects.get(device_uid = device_uid)
        except Device.DoesNotExist:
            return Response({
                "detail": "Invalid device credentials."
            }, status=401)

        if device.device_secret != device_secret:
            return Response({
                "detail": "Invalid device credentials."
            }, status=401)

        device.is_online = True
        device.last_seen = timezone.now()

        device.save(
            update_fields = [
                "is_online",
                "last_seen",
                "updated_at"
            ]
        )

        return Response({
            "message": "Heartbeat received.",
            "device_uid": device.device_uid,
            "is_online": device.is_online,
            "last_seen": device.last_seen
        }, status=200)
    
    
