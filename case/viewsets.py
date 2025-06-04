from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .models import Case, CaseAttachment, Comment
from .serializers import CaseSerializer, CaseAttachmentSerializer, CommentSerializer
from user.authentication import CookieTokenAuthentication 
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
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
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        return Case.objects.all()

    def perform_create(self, serializer):
        """Automatically attach the logged-in user to the case."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"], url_path="submit_case")
    def submit_case(self, request):
        print("Request data:", request.data)  # Debug: See all incoming data
        print("Request files:", request.FILES)  # Debug: See uploaded files
        case_data = {
            'title': request.data.get('title'),
            'case_type': request.data.get('case_type'),
            'description': request.data.get('description'),
            'status': 'open',
        }

        serializer = self.get_serializer(data=case_data)
        serializer.is_valid(raise_exception=True)
        case = serializer.save(created_by=request.user)
            
        files = request.FILES.getlist('files') 
        print(f"Number of files received: {len(files)}")  # Debug: Count files
        attachments = []

        for file in files:
            print(f"Processing file: {file.name}")  # Debug: File info
            attachment = CaseAttachment.objects.create(
                case=case,
                file=file,
                description=f"Uploaded with case submission"
            )
            attachments.append(attachment)
            print(f"Created attachment ID: {attachment.id}")  # Debug: Attachment ID

        # Serialize attachments separately
        attachment_serializer = CaseAttachmentSerializer(
            attachments,
            many=True,
            context={'request': request}
        )

        print("Serialized attachments:", attachment_serializer.data)  # Debug: Final output

        return Response(
            {
                "message": "Case submitted successfully!", 
                "case": serializer.data,
                "attachments": attachment_serializer.data,
            },
            status=status.HTTP_201_CREATED
        )        

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

    @action(detail=True, methods=['patch'], url_path="discarded")
    def discarded(self, request, pk=None):
        try:
            case = self.get_object()
            case.status = 'discarded'
            case.save()
            serializer = self.get_serializer(case)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Case.DoesNotExist:
            return Response({"success": False, "error": "Case not found"}, status=status.HTTP_404_NOT_FOUND)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication]

    def get_queryset(self):
        case_id = self.request.query_params.get('case_id')
        if case_id:
            return Comment.objects.filter(case_id=case_id).select_related('author')
        return Comment.objects.none()

    def perform_create(self, serializer):
        case_id = self.request.data.get('case')
        try:
            case = Case.objects.get(id=case_id)
            serializer.save(author=self.request.user, case=case)
        except Case.DoesNotExist:
            raise serializer.ValidationError("Case does not exist")