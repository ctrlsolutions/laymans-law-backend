from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()
print(User)

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None
        try:
            user = User.objects.get(email=email)
            print(f"User Found: {user}")
        except User.DoesNotExist:
            print("User not found")
            return None

        print(f"Password Match: {user.check_password(password)}")
        print(f"Can Authenticate: {self.user_can_authenticate(user)}")

        if user.check_password(password) and self.user_can_authenticate(user):
            print(user)
            return user

        return None


class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Get token from the `authToken` cookie
        token = request.COOKIES.get("authToken")
        print("Received authToken from cookies:", token)
        if not token:
            return None  # No token, return None so DRF tries other authentication methods

        return self.authenticate_credentials(token)
