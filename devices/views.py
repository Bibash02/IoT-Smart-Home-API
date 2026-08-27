from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  
from rest_framework import status
from rest_framework import generics

from .models import DeviceCommand, Device, DeviceToken
from .serializers import DeviceSerializer, DeviceCommandSerializer, DeviceAuthSerializer, DeviceHeartbeatSerializer, DeviceTokenSerializer
from .services import execute_device_command
from datetime import timezone
from django.db import transaction

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
            }, status=status.HTTP_401_UNAUTHORIZED)

        if device.device_secret != device_secret:
            return Response({
                "detail": "Invalid device credentials."
            }, status=status.HTTP_401_UNAUTHORIZED)

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

class DeviceCommandCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceCommandSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data = request.data
        )

        serializer.is_valid(raise_exception = True)

        device = serializer.validated_data['device']
        command_type = serializer.validated_data['command']
        value = serializer.validated_data.get('value')

        try:
            command = execute_device_command(
                device=device,
                command_type=command_type,
                value=value
            )
        except ValueError as error:
            return Response({
                'success': False,
                'error': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'message': 'Command executed successfully.',
            'data': DeviceCommandSerializer(
                command,
                context = {
                    'request': request
                }
            ).data
        },status=status.HTTP_201_CREATED)
      
class DeviceCommandListAPIView(generics.ListCreateAPIView):
    serializer_class = DeviceCommandSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeviceCommand.objects.filter(
            device__user = self.request.user
        ).select_related(
            'device'
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()

# class DeviceCommandDetailAPIView(generics.RetrieveAPIView):
#     serializer_class = DeviceCommandSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return DeviceCommand.objects.filter(device__user = self.request.user)

class DeviceCommandHistoryAPIView(generics.ListAPIView):
    serializer_class = DeviceCommandSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        device_id = self.kwargs['pk']

        return DeviceCommand.objects.filter(
            device_id = device_id,
            device__user = self.request.user
        ).select_related('device').order_by('-created_at')

class PendingDeviceCommandAPIView(generics.ListAPIView):
    serializer_class = DeviceCommandSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeviceCommand.objects.filter(
            device__user = self.request.user,
            status = DeviceCommand.CommandStatus.PENDING
        ).select_related(
            'device'
        ).order_by('created_at')

class ClaimDeviceCommandAPIView(generics.GenericAPIView):
    serializer_class = DeviceCommandSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        with transaction.atomic():
            try:
                command = (
                    DeviceCommand.objects
                    .select_for_update()
                    .select_related('device')
                    .get(
                        id = pk,
                        device__user = request.user,
                        status = DeviceCommand.CommandStatus.PENDING
                    )
                )
            except DeviceCommand.DoesNotExist:
                return Response({
                    "detail": "Pending command not found."
                }, status=404)

            command.status - (
                DeviceCommand.CommandStatus.PROCESSING
            )

            command.save(
                update_fields=['status']
            )

        return Response(
            DeviceCommandSerializer(command, context={'request': request}).data
        )

class DeviceCommandResultAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            command = DeviceCommand.objects.get(
                id = pk,
                device__user = self.request.user
            )
        except DeviceCommand.DoesNotExist:
            return Response({
                "detail": "Command not found."
            }, status=404)

        result_status = request.data.get('status')
        response_message = request.data.get('response', '')

        valid_status = [
            DeviceCommand.CommandStatus.SUCCESS,
            DeviceCommand.CommandStatus.FAILED
        ]

        if result_status not in valid_status:
            return Response({
                "detail": "Status must be SUCCESS or FAILED."
            }, status=400)

        if command.status != (DeviceCommand.CommandStatus.PROCESSING):
            return Response({
                "detail": "Command is not currently processing."
            }, status=400)

        command.status = result_status
        command.response = response_message
        command.executed_at = timezone.now()
        command.save(
            update_fields=[
                'status',
                'response',
                'executed_at'
            ]
        )

        return Response({
            "success": True,
            "command_id": command.id,
            'status': command.status,
            'response': command.response
        })

class DeviceTokenCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, device_id):
        try:
            device = Device.objects.get(id = device_id, user = request.user)
        except Device.DoesNotExist:
            return Response({
                "detail": "Device not found."
            }, status=404)

        token, created = DeviceToken.objects.get_or_create(device = device)

        if not created:
            token.token = DeviceToken().token
            token.is_active = True
            token.save(
                update_fields = [
                    'token',
                    'is_active'
                ]
            )

        return Response({
            "success": True,
            "message": "Device token generated.",
            "data": DeviceTokenSerializer(token).data
        }, status=201)