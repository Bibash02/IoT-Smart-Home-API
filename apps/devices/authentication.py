from django.utils import timezone

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import DeviceToken

class DeviceTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get(
            "X-DEVICE-TOKEN"
        )

        if not token:
            return None

        try:
            device_token = (
                DeviceToken.objects.select_related('device').get(token = token, is_active = True)
            )
        except DeviceToken.DoesNotExist:
            raise AuthenticationFailed("Invalid device token.")

        device_token.last_used_at = timezone.now()

        device_token.save(
            update_fields = [
                'last_used_at'
            ]
        )

        return (
            device_token.device,
            device_token
        )
