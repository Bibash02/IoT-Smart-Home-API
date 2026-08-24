from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import AutomationRule
from .serializers import AutomationRuleSerializer

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
    
    