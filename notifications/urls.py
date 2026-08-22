from django.urls import path
from .views import NotificationListAPIView, NotificationDetailAPIView, NotificationMarkReadAPIView, NotificationMarkAllReadAPIView

urlpatterns = [
    path('notification/list/', NotificationListAPIView.as_view(), name='notification-list'),
    path('notification/<int:pk>/detail/', NotificationDetailAPIView.as_view(), name='notification-detail'),
    path('notification/<int:pk>/mark-read/', NotificationMarkReadAPIView.as_view(), name='notification-mark-read'),
    path('notification/mark-read-all/', NotificationMarkAllReadAPIView.as_view(), name='notification-mark-read-all'),
]