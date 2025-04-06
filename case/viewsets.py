# case/viewsets.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Case
from .serializers import CaseSerializer, CaseSubmitSerializer
from user.authentication import CookieTokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response



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

    @action(detail=False, methods=["post"])
    def submit_case(self, request):
        """Submits a case"""
        print(request.user)
        if not hasattr(request.user, 'user_type') or request.user.user_type != 'layman':
            print("HERE")
            return Response({'detail': 'Only layman users can submit cases.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CaseSubmitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            print("its valid")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
