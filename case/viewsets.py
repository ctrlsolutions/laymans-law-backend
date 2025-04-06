# case/viewsets.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .models import Case
from .serializers import CaseSerializer
from user.authentication import CookieTokenAuthentication  # Import the custom authentication class
from rest_framework.authentication import TokenAuthentication

class CaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']  
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication]  # Add custom authentication

    def get_queryset(self):
        return Case.objects.all()

    def perform_create(self, serializer):
        """Automatically attach the logged-in user to the case."""
        serializer.save(user=self.request.user)
