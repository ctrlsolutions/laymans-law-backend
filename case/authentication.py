from rest_framework.authentication import TokenAuthentication

class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('authToken')  # Read 'authToken' from cookies
        if token:
            return self.authenticate_credentials(token)
        return None
