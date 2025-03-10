from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from rest_framework.authentication import SessionAuthentication

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email')  # Handle email authentication

        try:
            user = User.objects.get(email=username)  # Fetch user by email
            if user.check_password(password):  # Validate password
                return user
        except User.DoesNotExist:
            return None



class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # Disable CSRF check for API requests
