from django.urls import path
from .views import AutomationRuleListCreateAPIView, AutomationRuleDetailAPIView, AutomationRuleToggleAPIView

urlpatterns = [
    path('automation/', AutomationRuleListCreateAPIView.as_view(), name='automation-list-create'),
    path('automation/<int:pk>/', AutomationRuleDetailAPIView.as_view(), name='automation-detail'),
    path('automation/<int:pk>/toggle/', AutomationRuleToggleAPIView.as_view(), name='automation-toggle'),
]