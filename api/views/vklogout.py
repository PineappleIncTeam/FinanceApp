# views.py
import requests
from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.serializers.vklogout import LogoutRequestSerializer, LogoutResponseSerializer
from api.serializers.profile import ErrorSerializer


class LogoutView(GenericAPIView):
    serializer_class = LogoutResponseSerializer

    @swagger_auto_schema(
        operation_id="Выход из аккаунта пользователя",
        operation_description="Метод завершает сессию пользователя через VK API и инвалидирует токен",
        request_body=LogoutRequestSerializer,
        responses={
            200: openapi.Response(description="Сессия успешно завершена", schema=LogoutResponseSerializer),
            400: openapi.Response(description="Некорректный запрос", schema=ErrorSerializer),
            401: openapi.Response(description="Неавторизованный запрос", schema=ErrorSerializer),
            403: openapi.Response(description="Доступ запрещен", schema=ErrorSerializer),
            500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
            503: openapi.Response(description="Сервер временно недоступен", schema=ErrorSerializer),
        },
    )
    def post(self, request, *args, **kwargs):
        client_id = request.data.get("client_id")
        access_token = request.data.get("access_token") or request.headers.get("Authorization")

        if access_token and access_token.startswith("Bearer "):
            access_token = access_token.split(" ")[1]

        if not client_id:
            return Response(
                {"error": "invalid_client", "error_description": "client_id не передан"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not access_token:
            return Response(
                {"error": "invalid_token", "error_description": "Access token не передан"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            vk_response = requests.post(
                "https://id.vk.ru/oauth2/logout", data={"client_id": client_id, "access_token": access_token}, timeout=5
            )
        except requests.RequestException:
            return Response(
                {"error": "server_error", "error_description": "Не удалось связаться с сервером авторизации VK"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if vk_response.status_code == 200:
            data = vk_response.json()
            if data.get("response") == 1:
                return Response({"response": 1}, status=status.HTTP_200_OK)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                return Response(vk_response.json(), status=vk_response.status_code)
            except ValueError:
                return Response(
                    {"error": "server_error", "error_description": "Некорректный ответ от VK API"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
