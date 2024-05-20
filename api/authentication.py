from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("token")

        if not token:
            return None

        if len(token.split()) != 1:
            msg = "Invalid token in httponly cookies. No credentials provided."
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
