from rest_framework import serializers, viewsets
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import JsonResponse
from .models import CustomUser
from .serializers import LoginSerializer

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message": "Login successful!"})
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({"message": "Logged out successfully!"})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def user(self, request):
        serializer = LoginSerializer(request.user)
        return Response(serializer.data)
