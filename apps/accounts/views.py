from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Create your views here.
@api_view(['GET'])
def test(request):
    return Response("Successfully connected to the API.")

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user = user)

        return Response({
            'message': "Account created successfully.",
            'token': token.key,
            'username': user.username,
            'email': user.email,
        }, status=201)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
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