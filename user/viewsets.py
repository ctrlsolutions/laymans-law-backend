from rest_framework import viewsets
from django.db.utils import IntegrityError
from rest_framework import status

from .models import CustomUser, Lawyer

from .serializers import SignUpSerializer, LoginSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework.authtoken.models import Token


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
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "Login successful!", "token": token.key})
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({"message": "Logged out successfully!"})
    
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def signup(self, request):
        """Handles user registration based on user_type (Lawyer or Layman)"""
        print("Signup request received:", request.data)  # Debugging

        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.save()  # ✅ Creates user (and Lawyer if needed)
                return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)

            except IntegrityError:
                return Response({"error": "User with this email or roll number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def user(self, request):
        serializer = LoginSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='profile', permission_classes=[IsAuthenticated])
    def profile(self, request):
        user = request.user
        # user = CustomUser.objects.filter(email="johndoe@gmail.com")  # Get the logged-in user
        print(user)
        return Response({
            "first_name": user.first_name, 
            "last_name": user.last_name, 
            "email": user.email, 
            "contact_number": user.contact_number, 
            "gender": user.gender, 
            "birth_date": user.birth_date, 
            "user_type": user.user_type
        })

