from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()

class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None

        try:
            validated_token = AccessToken(token)
            user_id = validated_token['user_id']
            user = User.objects.get(id=user_id)
            return (user, validated_token)
        except Exception:
            raise AuthenticationFailed('Невалидный токен')
