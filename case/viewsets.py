from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Case
from .serializers import CaseSerializer
from user.authentication import CookieTokenAuthentication
from rest_framework.authentication import TokenAuthentication

class CaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']  
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieTokenAuthentication, TokenAuthentication] 

    def get_queryset(self):
        """
        Filter queryset based on user role and query parameters.
        - Laymen see their submitted cases.
        - Lawyers see 'available' cases by default, or their 'active' cases via query param.
        - Add more filters as needed (e.g., status, type).
        """
        user = self.request.user
        queryset = Case.objects.select_related('created_by', 'assigned_to').all()

        is_lawyer = getattr(user, 'is_lawyer', False)

        if is_lawyer:
            view_type = self.request.query_params.get('view', 'available') # Default view for lawyers
            if view_type == 'active':
                # Show cases assigned to this lawyer
                queryset = queryset.filter(assigned_to=user, status='active')
            elif view_type == 'available':
                # Show open cases not assigned to anyone
                queryset = queryset.filter(status='open', assigned_to__isnull=True)
            # Add other views for lawyers if needed (e.g., 'closed')
            # else: return all cases visible to lawyer? or specific permission based view?
            # For now, if not 'active' or 'available', show 'available'
            else:
                 queryset = queryset.filter(status='open', assigned_to__isnull=True)

        else: # User is a layman
             # Laymen only see cases they created
             queryset = queryset.filter(created_by=user)

        case_type = self.request.query_params.get('case_type')
        if case_type:
            queryset = queryset.filter(case_type=case_type)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)


        return queryset.order_by('-created_date') # Order by most recent

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
        case.status = 'active'
        case.accepted_date = timezone.now()
        case.save()

        serializer = self.get_serializer(case)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # --- Add other custom actions if needed ---
    # Example: Action for a lawyer to close/resolve a case
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def close(self, request, pk=None):
         case = self.get_object()
         # Check if the requesting lawyer is the assigned lawyer
         if case.assigned_to != request.user:
              return Response(
                   {'detail': 'You are not assigned to this case.'},
                   status=status.HTTP_403_FORBIDDEN
              )
         if case.status == 'closed':
              return Response(
                   {'detail': 'Case is already closed.'},
                   status=status.HTTP_400_BAD_REQUEST
              )

         case.status = 'closed'
         # Maybe add a 'closed_date' field?
         case.save()
         serializer = self.get_serializer(case)
         return Response(serializer.data, status=status.HTTP_200_OK)
