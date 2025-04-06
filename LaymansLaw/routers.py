from rest_framework import routers
from user.viewsets import AuthViewSet
from case.viewsets import CaseViewSet

router = routers.SimpleRouter()

router.register(r'user', AuthViewSet, basename="user")
router.register(r'cases', CaseViewSet, basename="case")

urlpatterns = router.urls