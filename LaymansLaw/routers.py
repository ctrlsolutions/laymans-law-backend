from rest_framework.routers import DefaultRouter
from user.viewsets import CustomUserViewSet  # Adjust this import based on your app name

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='customuser')

urlpatterns = router.urls

