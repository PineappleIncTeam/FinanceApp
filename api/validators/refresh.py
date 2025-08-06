from rest_framework.authentication import BaseAuthentication

class NoOpAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print("🚫 NoOpAuthentication вызвана!")
        return None