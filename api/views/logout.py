from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.serializers.logout import LogoutSerializer


class CustomLogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id='Выход из аккаунта',
        operation_description='Выход из аккаунта',
        responses={
            200: openapi.Response(description="Выход успешно выполнен"),
            401: openapi.Response(description="Неавторизованный запрос")
        }
    )
    def post(self, request):
        response = Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK
        )
        response.delete_cookie('access_token', path='/', domain=None)
        response.delete_cookie('refresh_token', path='/', domain=None)

        for cookie_name in request.COOKIES:
            response.delete_cookie(cookie_name)

        return response