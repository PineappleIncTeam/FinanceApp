import requests
from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.serializers.vkchecktoken import (
    VKCheckTokenRequestSerializer,
    VKCheckTokenResponseSerializer,
)
from api.serializers.profile import ErrorSerializer


class VKCheckTokenView(GenericAPIView):
    """
    POST /api/v1/vk/check-token/
    Проверяет валидность access_token пользователя через VK API (secure.checkToken)
    """

    serializer_class = VKCheckTokenResponseSerializer

    @swagger_auto_schema(
        operation_id="Валидация токена VK",
        operation_description="Метод проверяет, что access_token пользователя выдан именно этому приложению",
        request_body=VKCheckTokenRequestSerializer,
        responses={
            200: openapi.Response(description="Токен успешно проверен", schema=VKCheckTokenResponseSerializer),
            400: openapi.Response(description="Некорректный запрос", schema=ErrorSerializer),
            401: openapi.Response(description="Неавторизованный запрос", schema=ErrorSerializer),
            500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        },
    )
    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        ip = request.data.get("ip")

        if not token:
            return Response(
                {"error": "invalid_token", "error_description": "Access token не передан"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        params = {"token": token, "access_token": settings.VK_SERVICE_KEY, "v": "5.131"}  # сервисный ключ доступа
        if ip:
            params["ip"] = ip

        try:
            vk_response = requests.get("https://api.vk.com/method/secure.checkToken", params=params, timeout=5)
        except requests.RequestException:
            return Response(
                {"error": "server_error", "error_description": "Не удалось связаться с VK API"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        data = vk_response.json()

        if "response" in data:
            return Response(data["response"], status=status.HTTP_200_OK)
        else:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
