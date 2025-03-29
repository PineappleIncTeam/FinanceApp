from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token

from api.serializers.profile import ErrorSerializer


class CustomLogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='Выход из аккаунта',
        operation_description='Выход из аккаунта',
        responses={
        200: openapi.Response(description="Выход успешно выполнен"),
        401: openapi.Response(description="Неавторизованный запрос")
    })
    def post(self, request):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()

        response = Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK
        )
        cookies = request.COOKIES
        for i in cookies:
            response.delete_cookie(i)

        return response