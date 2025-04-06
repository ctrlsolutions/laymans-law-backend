# case/urls.py
from django.urls import path, include
from .routers import router  # Import the router

urlpatterns = [
    path('', include(router.urls)),  # Just include the router
]
