from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import os
from dotenv import load_dotenv
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
load_dotenv()
User = get_user_model()

class VKOAuth2View(APIView):
    @swagger_auto_schema(
        operation_description="Обмен VK-кода на Django-совместимые токены и создание/обновление пользователя.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["code", "code_verifier", "device_id"],
            properties={
                "code": openapi.Schema(type=openapi.TYPE_STRING),
                "code_verifier": openapi.Schema(type=openapi.TYPE_STRING),
                "device_id": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(description="Успешно", examples={
                "application/json": {
                    "access": "jwt_access_token",
                    "refresh": "jwt_refresh_token",
                    "user": {
                        "id": 1,
                        "username": "vk_1234567890",
                        "first_name": "Ivan",
                        "last_name": "Ivanov",
                        "avatar": "https://example.com/avatar.png"
                    }
                }
            }),
            400: openapi.Response(description="Ошибка запроса"),
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

        vk_response = requests.post(vk_api_url, data=payload)
        if vk_response.status_code != 200:
            return Response({"error": "Failed to exchange code"}, status=vk_response.status_code)

        tokens = vk_response.json()
        access_token = tokens.get("access_token")
        if not access_token:
            return Response({"error": "No access token received"}, status=status.HTTP_403_FORBIDDEN)

        user_info_url = "https://id.vk.com/oauth2/user_info"
        user_info_payload = {
            "access_token": access_token,
            "client_id": os.getenv("CLIENT_ID")
        }
        user_info_response = requests.post(user_info_url, data=user_info_payload)
        if user_info_response.status_code != 200:
            return Response({"error": "Failed to fetch user info"}, status=user_info_response.status_code)

        vk_user = user_info_response.json()
        vk_id = vk_user.get("user_id")
        username = f"vk_{vk_id}"

        user, created = User.objects.get_or_create(username=username, defaults={
            "first_name": vk_user.get("first_name", ""),
            "last_name": vk_user.get("last_name", ""),
        })

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar": vk_user.get("avatar"),
            }
        }, status=status.HTTP_200_OK)
