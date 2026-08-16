from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from rest_framework import status

from .models import DeviceCommand, Device
from .serializers import DeviceSerializer, DeviceCommandSerializer
from .services import execute_device_command

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