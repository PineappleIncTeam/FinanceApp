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
        operation_description="Обмен кода авторизации на токены VK и получение личных данных пользователя.",
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
                        "user_info": {
                            "user_id": "1234567890",
                            "first_name": "Ivan",
                            "last_name": "Ivanov",
                            "phone": "79991234567",
                            "avatar": "https://pp.userapi.com/60tZWMo4SmwcploUVl9XEt8ufnTTvDUmQ6Bj1g/mmv1pcj63C4.png",
                            "email": "ivan_i123@vk.com",
                            "sex": 2,
                            "verified": False,
                            "birthday": "01.01.2000"
                        }
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

        vk_api_url = "https://id.vk.com/oauth2/token"
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
        access_token = tokens.get("access_token")

        if not access_token:
            return Response({"error": "No access token received"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Получение личных данных пользователя
        user_info_url = "https://id.vk.com/oauth2/user_info"
        user_info_payload = {
            "access_token": access_token,
            "client_id": os.getenv("CLIENT_ID")
        }
        user_info_response = requests.post(user_info_url, data=user_info_payload)

        if user_info_response.status_code != 200:
            return Response({"error": "Failed to fetch user info"}, status=user_info_response.status_code)

        user_info = user_info_response.json()

        return Response(
            {
                "access_token": access_token,
                "refresh_token": tokens["refresh_token"],
                "id_token": tokens["id_token"],
                "user_info": user_info,
            },
            status=status.HTTP_200_OK,
        )
