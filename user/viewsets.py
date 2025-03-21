from rest_framework import viewsets
from django.db.utils import IntegrityError
from rest_framework import status

from .models import CustomUser

from .serializers import SignUpSerializer, LoginSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import login, logout

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            print(f"User {user.email} successfully logged in!")
            return Response({"message": "Login successful!"})
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({"message": "Logged out successfully!"})
    
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def signup(self, request):
        print("Signup request received!")
        print("Request data:", request.data)  # Debugging
        serializer = SignUpSerializer(data=request.data)
                
        if serializer.is_valid():
            try:
                serializer.save() 
                return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
