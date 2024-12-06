from django.http import JsonResponse
from djoser.utils import login_user
from djoser.views import TokenCreateView


class CustomTokenCreateAPI(TokenCreateView):
    """

    """
    def _action(self, serializer):
        token = login_user(self.request, serializer.user)
        response = JsonResponse({"token": token.key})
        response.set_cookie("token", token.key, httponly=True)
        return response
