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
