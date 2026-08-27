from rest_framework.permissions import BasePermission
from .models import DeviceToken

class IsIoDevice(BasePermission):
    def has_permission(self, request, view):
        return (
            request.auth is not None
            and isinstance(
                request.auth, DeviceToken
            )
        )