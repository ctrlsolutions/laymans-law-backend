from rest_framework import routers

from user.viewsets import AuthViewSet

router = routers.SimpleRouter()

router.register(r'user', AuthViewSet, basename="user")

urlpatterns = router.urls