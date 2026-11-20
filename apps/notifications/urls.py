from django.urls import path
from .views import NotificationListAPIView, NotificationDetailAPIView, NotificationMarkReadAPIView, NotificationMarkAllReadAPIView, UnreadNotificationcountAPIView, MarkNotificationReadAPIView, MarkAllNotificationReadAPIView

urlpatterns = [
    path('notification/list/', NotificationListAPIView.as_view(), name='notification-list'),
    path('notification/<int:pk>/detail/', NotificationDetailAPIView.as_view(), name='notification-detail'),
    path('notification/<int:pk>/mark-read/', NotificationMarkReadAPIView.as_view(), name='notification-mark-read'),
    path('notification/mark-read-all/', NotificationMarkAllReadAPIView.as_view(), name='notification-mark-read-all'),

    path('notification/unread-count/', UnreadNotificationcountAPIView.as_view(), name='unread-count'),
    path('notification/<int:pk>/read/', MarkAllNotificationReadAPIView.as_view(), name='notification-read'),
    path('notification/read-all/', MarkAllNotificationReadAPIView.as_view(), name='notification-read-all'),
]