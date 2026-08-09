from django.urls import path
from .views import *

urlpatterns = [
    path('test/', test, name='test'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]