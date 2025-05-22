from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .models import Case
from .serializers import CaseSerializer
from user.authentication import CookieTokenAuthentication 
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status

class CaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']  
    queryset = Case.objects.all().select_related('created_by')
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication] 
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return Case.objects.all()

    def perform_create(self, serializer):
        """Automatically attach the logged-in user to the case."""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def accept(self, request, pk=None):
        """
        Allows a lawyer user to accept an 'open' case.
        """
        case = self.get_object()

        if case.status != 'open' or case.assigned_to is not None:
            return Response(
                {'detail': 'This case is not available for acceptance.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        lawyer = request.user
        case.assigned_to = lawyer
        case.status = 'ongoing'
        case.accepted_date = timezone.now()
        case.save()

        serializer = self.get_serializer(case)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # --- Add other custom actions if needed ---
    # Example: Action for a lawyer to close/resolve a case
    @action(detail=True, methods=['patch'], url_path="close")
    def close(self, request, pk=None):
        try:
            case = self.get_object()
            case.status = "closed"
            case.save()
            serializer = self.get_serializer(case)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Case.DoesNotExist:
            return Response({"success": False, "error": "Case not found"}, status=status.HTTP_404_NOT_FOUND)
