from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import AutomationRule, AutomationExecution
from .serializers import AutomationRuleSerializer, AutomationExecutionSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class AutomationRuleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AutomationRuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AutomationRule.objects.filter(user = self.request.user).select_related('sensor', 'device')

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class AutomationRuleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AutomationRuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AutomationRule.objects.filter(user = self.request.user)
    
class AutomationRuleToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            rule = AutomationRule.objects.get(id = pk, user = request.user)
        except AutomationRule.DoesNotExist:
            return Response({
                "detail": "Automation Rule not found."
            }, status=status.HTTP_404_NOT_FOUND)

        rule.is_enabled = not rule.is_enabled
        rule.save(update_fields=['is_enabled', 'updated_at'])

        return Response({
            "message": "Automation rule updated.",
            "id": rule.id,
            "name": rule.name,
            "is_enabled": rule.is_enabled
        }, status=status.HTTP_200_OK)

class AutomationExecutionListAPIView(generics.ListAPIView):
    serializer_class = AutomationExecutionSerializer
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        return AutomationExecution.objects.filter(
            rule__user = self.request.user
        ).select_related(
            'rule',
            'device',
            'command'
        ).order_by('-executed_at')

class AutomationRuleExecutionListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AutomationExecutionSerializer

    def get_queryset(self):
        rule_id = self.kwargs['pk']

        return AutomationExecution.objects.filter(
            rule_id = rule_id,
            rule__user = self.request.user
        ).select_related(
            'rule',
            'device',
            'command'
        ).order_by('-executed_at')