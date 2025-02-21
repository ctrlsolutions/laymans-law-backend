from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication

from .models import CustomUser

from .serializers import CustomUserSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def csrf(self, request):
        return JsonResponse({"message": "CSRF cookie set"})
    
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        """Logs in a user and starts a session."""
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return Response({"message": "Login successful!"})
        return Response({"error": "Invalid credentials"}, status=401)
    
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logs out a user and destroys the session."""
        logout(request)
        return Response({"message": "Logged out successfully!"})
    
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def user(self, request):
        """Gets the authenticated user."""
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)
    
    # Signup action
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def signup(self, request):
        print("Request data:", request.data)  # Debugging
        serializer = CustomUserSerializer(data=request.data)
                
        if serializer.is_valid():
            print("Validated data:", serializer.validated_data)
            serializer.save() 
            return Response({"message": "User created successfully!"}, status=201)
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=400)