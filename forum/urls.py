from django.urls import path, include
from .routers import router  # import your router

urlpatterns = [
    path('api/', include(router.urls)),
]
