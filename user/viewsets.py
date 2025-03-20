from rest_framework import serializers, viewsets
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import JsonResponse
from .models import CustomUser
from .serializers import LoginSerializer
from rest_framework.authentication import TokenAuthentication
from .authentication import CsrfExemptSessionAuthentication
from rest_framework.authtoken.models import Token 
from .serializers import UserSerializer

class AuthViewSet(viewsets.ViewSet):
    authentication_classes = [CsrfExemptSessionAuthentication, TokenAuthentication]
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            # Generate or get existing token
            token, created = Token.objects.get_or_create(user=user)

            print(f"User {user.email} successfully logged in! Token: {token.key}")

            # Send token in response
            return Response({"message": "Login successful!", "token": token.key})
        
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.auth.delete()  # Delete token on logout
        logout(request)
        return Response({"message": "Logged out successfully!"})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def user(self, request):
        if not request.user:
            return Response({"error": "User not found"}, status=404)
        
        return Response({
            "email": request.user.email,
            "firstName": request.user.first_name,
            "lastName": request.user.last_name,
            "birth_date": str(request.user.birth_date) if request.user.birth_date else None,  # Ensure JSON serializable
            "contact_number": request.user.contact_number,
            "gender": request.user.gender
        })