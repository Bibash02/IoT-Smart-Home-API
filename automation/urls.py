from django.urls import path
from .views import AutomationRuleListCreateAPIView, AutomationRuleDetailAPIView, AutomationRuleToggleAPIView

urlpatterns = [
    path('automation/', AutomationRuleListCreateAPIView.as_view(), name='automation-list-create'),
    path('automation/<pk:id>/', AutomationRuleDetailAPIView.as_view(), name='automation-detail'),
    path('automation/<pk:id>/toggle/', AutomationRuleToggleAPIView.as_view(), name='automation-toggle'),
]