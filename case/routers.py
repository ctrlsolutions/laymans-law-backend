# case/routers.py
from rest_framework.routers import DefaultRouter
from .viewsets import CaseViewSet

router = DefaultRouter()
router.register(r'', CaseViewSet, basename='case')
