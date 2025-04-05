from rest_framework import viewsets
from django.db.utils import IntegrityError
from rest_framework import status

from .serializers import SignUpSerializer, LoginSerializer, UserProfileSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.http import JsonResponse    
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .authentication import CookieTokenAuthentication

from django.contrib.auth import login, logout

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    @method_decorator(ensure_csrf_cookie)
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def csrf(self, request):
        return JsonResponse({"message": "CSRF cookie set"})

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            print(f"User {user.email} successfully logged in!")
            token, _ = Token.objects.get_or_create(user=user)
            response = JsonResponse({"message": "Login successful!", "user_id": user.user_id, "user_type": user.user_type})
            response.set_cookie("authToken", token.key, httponly=True, samesite="None", secure=True)
            return response 
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], authentication_classes=[CookieTokenAuthentication, TokenAuthentication])
    def logout(self, request):
        if isinstance(request.auth, Token):
            request.auth.delete()
        logout(request)
        return Response({"message": "Logged out successfully!"}, status=200)
    
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def signup(self, request):
        """Handles user registration based on user_type (Lawyer or Layman)"""
        print("Signup request received:", request.data)

        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)

            except IntegrityError:
                return Response({"error": "User with this email or roll number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], authentication_classes = [CookieTokenAuthentication, TokenAuthentication])
    def get_profile(self, request):
        user = request.user
        print(user, user.first_name, user.last_name, user.email, user.contact_number, user.gender, user.birth_date, user.user_type)
        return Response({
            "first_name": user.first_name, 
            "last_name": user.last_name, 
            "email": user.email, 
            "contact_number": user.contact_number, 
            "gender": user.gender, 
            "birth_date": user.birth_date, 
            "user_type": user.user_type
        })
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated], authentication_classes = [CookieTokenAuthentication, TokenAuthentication])
    def update_profile(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

