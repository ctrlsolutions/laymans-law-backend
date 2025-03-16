from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

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
