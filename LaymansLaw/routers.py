from rest_framework import routers
from user.viewsets import AuthViewSet
from case.viewsets import CaseViewSet
from wiki.viewsets import LawViewSet, OFWSupportDetailViewSet

router = routers.SimpleRouter()

router.register(r'user', AuthViewSet, basename="user")
router.register(r'cases', CaseViewSet, basename="case")
router.register(r'laws', LawViewSet, basename="law")
router.register(r'ofw-support', OFWSupportDetailViewSet, basename="ofw")

urlpatterns = router.urls