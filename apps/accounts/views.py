from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework.authtoken.models import Token

# Create your views here.
@api_view(['GET'])
def test(request):
    return Response("Successfully connected to the API.")

class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(request=RegisterSerializer)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user = user)

        return Response({
            'message': "Account created successfully.",
            'token': token.key,
            'username': user.username,
            'email': user.email,
        }, status=201)

class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user_obj = User.objects.get(email = email)
        except User.DoesNotExist:
            return Response({
                "error": "Invalid email or password"
            }, status=404)

        user = authenticate(username = user_obj.username, password = password)

        if not user:
            return Response({
                "error": "Invalid email or password"
            }, status=404)

        token, _ = Token.objects.get_or_create(user = user)

        return Response({
            "message": "Login Successfully.",
            "token": token.key,
            "username": user.username
        })
