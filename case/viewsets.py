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

    @action(detail=False, methods=["post"], url_path="submit_case")
    def submit_case(self, request):

        case_data = {
            'title': request.data.get('title'),
            'case_type': request.data.get('case_type'),
            'description': request.data.get('description'),
        }

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            case = serializer.save()
            
            files = request.FILES.getlist('files') 

            for file in files:
                if file.content_type.startswith('image/'):
                    case.image = file
                elif file.content_type.startswith('video/'):
                    case.video = file
                else:
                    case.document = file
                case.save()

            return Response({"message": "Case submitted successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    
    @action(detail=True, methods=['delete'], url_path="delete")
    def delete(self, request, pk=None):
        try:
            case = self.get_object()
            case.delete()
            return Response({"success": True, "message": "Case deleted successfully"}, status=status.HTTP_200_OK)
        except Case.DoesNotExist:
            return Response({"success": False, "error": "Case not found"}, status=status.HTTP_404_NOT_FOUND)
