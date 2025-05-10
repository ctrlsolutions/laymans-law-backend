from rest_framework.routers import DefaultRouter
from .viewsets import ForumViewSet

router = DefaultRouter()
router.register(r'forum', ForumViewSet, basename='forum')

urlpatterns = router.urls
