from django.urls import path
from .views import *

urlpatterns = [
    path('room/', RoomListCreateAPIView.as_view(), name='room-list-create'),
    path('room/<int:pk>/', RoomRetrieveUpdateDestroyAPIView.as_view(), name='room-retrieve-update-destroy'),
]