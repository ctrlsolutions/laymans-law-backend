# case/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CaseViewSet  # Import your viewset

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'', CaseViewSet, basename='case')

urlpatterns = [
    path('', include(router.urls)),  # Include the router's URLs
]
