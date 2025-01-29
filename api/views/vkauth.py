from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

import os

from dotenv import load_dotenv
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


load_dotenv()


class VKOAuth2View(APIView):
    @swagger_auto_schema(
        operation_description="Обмен кода авторизации на токены VK.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["code", "code_verifier", "device_id"],
            properties={
                "code": openapi.Schema(type=openapi.TYPE_STRING, description="Код авторизации, полученный от VK"),
                "code_verifier": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Строка, использованная для защиты PKCE"
                ),
                "device_id": openapi.Schema(type=openapi.TYPE_STRING, description="Идентификатор устройства"),
            },
        ),
        responses={
            200: openapi.Response(
                description="Успешный ответ",
                examples={
                    "application/json": {
                        "access_token": "vk2.a.access_token_example",
                        "refresh_token": "vk2.a.refresh_token_example",
                        "id_token": "id_token_example",
                    }
                },
            ),
            400: openapi.Response(description="Неверные параметры запроса"),
            500: openapi.Response(description="Ошибка сервера"),
        },
    )
    def post(self, request):
        code = request.data.get("code")
        code_verifier = request.data.get("code_verifier")
        device_id = request.data.get("device_id")

        if not code or not code_verifier or not device_id:
            return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

        vk_api_url = "https://id.vk.com/oauth2/auth"
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "code_verifier": code_verifier,
            "device_id": device_id,
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CL_SECRET"),
            "redirect_uri": os.getenv("REDIRECT_URI"),
        }

        response = requests.post(vk_api_url, data=payload)

        if response.status_code != 200:
            return Response({"error": "Failed to exchange code"}, status=response.status_code)

        tokens = response.json()
        print("Response from VK API:", tokens)

        return Response(
            {
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "id_token": tokens["id_token"],
            },
            status=status.HTTP_200_OK,
        )
