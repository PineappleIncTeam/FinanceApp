import os
import logging
import requests
from dotenv import load_dotenv
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.views.vkchecktoken import VKCheckTokenView

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
            200: openapi.Response(description="Успешно"),
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

        vk_token_url = "https://id.vk.com/oauth2/auth"
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "code_verifier": code_verifier,
            "device_id": device_id,
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CL_SECRET"),
            "redirect_uri": os.getenv("REDIRECT_URI"),
        }

        try:
            vk_response = requests.post(vk_token_url, data=payload, timeout=5)
        except requests.RequestException:
            return Response({"error": "Failed to reach VK token endpoint"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if vk_response.status_code != 200:
            return Response(vk_response.json(), status=vk_response.status_code)

        tokens = vk_response.json()
        access_token = tokens.get("access_token")
        refresh_token_vk = tokens.get("refresh_token")
        if not access_token:
            return Response({"error": "No access token received"}, status=status.HTTP_403_FORBIDDEN)

        # Проверка токена через secure.checkToken
        factory = APIRequestFactory()
        check_req = factory.post("/api/v1/vk/check-token/", {"token": access_token}, format="json")
        check_view = VKCheckTokenView.as_view()

        try:
            check_response = check_view(check_req)
        except Exception as exc:
            logger.exception("VKCheckTokenView check failed: %s", exc)
            return Response({"error": "server_error", "error_description": "Token validation failed"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if getattr(check_response, "status_code", None) != 200:
            return Response({"error": "invalid_token", "detail": getattr(check_response, "data", None)},
                            status=status.HTTP_403_FORBIDDEN)

        # Получаем инфо о пользователе
        user_info_url = "https://id.vk.com/oauth2/user_info"
        user_info_payload = {"access_token": access_token, "client_id": os.getenv("CLIENT_ID")}
        try:
            user_info_response = requests.post(user_info_url, data=user_info_payload, timeout=5)
        except requests.RequestException:
            return Response({"error": "Failed to fetch user info"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if user_info_response.status_code != 200:
            return Response(user_info_response.json(), status=user_info_response.status_code)

        vk_user = user_info_response.json()
        vk_id = vk_user.get("sub") or vk_user.get("id")
        username = f"vk_{vk_id}" if vk_id else None
        email = vk_user.get("email") or f"{vk_id}@vk.local"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": vk_user.get("first_name", ""),
                "last_name": vk_user.get("last_name", ""),
                "email": email,
            },
        )

        # JWT токены
        refresh = RefreshToken.for_user(user)
        access_token_jwt = str(refresh.access_token)
        refresh_token_jwt = str(refresh)

        response_data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar": vk_user.get("picture"),
            }
        }
        resp = Response(response_data, status=status.HTTP_200_OK)


        # Настройки времени жизни
        try:
            access_lifetime = jwt_settings.ACCESS_TOKEN_LIFETIME
            refresh_lifetime = jwt_settings.REFRESH_TOKEN_LIFETIME
            access_max_age = int(access_lifetime.total_seconds())
            refresh_max_age = int(refresh_lifetime.total_seconds())
        except Exception:
            access_max_age = 3600
            refresh_max_age = 60 * 60 * 24 * 7

        secure_flag = not getattr(settings, "DEBUG", False)

        # JWT куки
        resp.set_cookie("jwt_access", access_token_jwt, httponly=True, secure=secure_flag,
                        samesite="Lax", max_age=access_max_age, path="/")
        resp.set_cookie("jwt_refresh", refresh_token_jwt, httponly=True, secure=secure_flag,
                        samesite="Lax", max_age=refresh_max_age, path="/")

        # VK куки
        resp.set_cookie("vk_access", access_token, httponly=True, secure=secure_flag,
                        samesite="Lax", max_age=int(tokens.get("expires_in", access_max_age)), path="/")
        if refresh_token_vk:
            resp.set_cookie("vk_refresh", refresh_token_vk, httponly=True, secure=secure_flag,
                            samesite="Lax", max_age=int(tokens.get("expires_in", refresh_max_age)), path="/")

        # Кэшируем токены
        vk_ttl = tokens.get("expires_in") or access_max_age
        cache.set(f"vk_tokens:{vk_id}", tokens, timeout=int(vk_ttl))
        cache.set(f"jwt_tokens:{user.id}", {"access": access_token_jwt, "refresh": refresh_token_jwt},
                  timeout=refresh_max_age)

        return resp
