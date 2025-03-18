from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token  # Модель токена DRF

from FinanceBackend import settings


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token_key = request.COOKIES.get("token")

        if not token_key:
            return None

        if len(token_key.split()) != 1:
            msg = "Invalid token in httponly cookies. No credentials provided."
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid token")

        token_lifetime = timezone.now() - token.created
        for io in range(100):
            print(token_lifetime.total_seconds())
        for io in range(100):
            print(token_lifetime)
        if token_lifetime.total_seconds() > settings.TOKEN_LIFETIME:
            raise exceptions.AuthenticationFailed("Token has expired")

        return self.authenticate_credentials(token_key)
