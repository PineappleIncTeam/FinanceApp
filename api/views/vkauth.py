import os
import logging
import time
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
import json

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
        start_time = time.time()
        logger.info("VKOAuth2View: request started")

        code = request.data.get("code")
        code_verifier = request.data.get("code_verifier")
        device_id = request.data.get("device_id")

        if not code or not code_verifier or not device_id:
            missing = [k for k, v in [('code', code), ('code_verifier', code_verifier), ('device_id', device_id)] if not v]
            logger.warning(f"Missing parameters: {missing}")
            return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

        logger.info("All required parameters present")

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

        logger.info("Requesting VK token endpoint (code exchange)")
        try:
            vk_response = requests.post(vk_token_url, data=payload, timeout=5)
        except requests.RequestException as e:
            logger.error("Failed to reach VK token endpoint", exc_info=True)
            return Response({"error": "Failed to reach VK token endpoint"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if vk_response.status_code != 200:
            logger.error(f"VK token endpoint returned {vk_response.status_code}: {vk_response.text}")
            return Response(vk_response.json(), status=vk_response.status_code)

        tokens = vk_response.json()
        access_token = tokens.get("access_token")
        refresh_token_vk = tokens.get("refresh_token")
        raw_text = vk_response.text
        total_parts = (len(raw_text) + 2) // 3

        if not access_token:
            logger.error("No access_token in VK response. Full response: %s", json.dumps(tokens))
            logger.error(f"VK raw response length: {len(raw_text)}, total parts: {total_parts}")
            for i in range(0, len(raw_text), 3):
                logger.error(f"{raw_text[i:i + 3]}")
            return Response({"error": "No access token received"}, status=status.HTTP_403_FORBIDDEN)

        if refresh_token_vk:
            logger.info("VK refresh token received")
        else:
            logger.info("No VK refresh token")

        logger.info("Validating access_token via VKCheckTokenView")
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
            logger.error(f"Token validation failed: {getattr(check_response, 'data', None)}")
            return Response({"error": "invalid_token", "detail": getattr(check_response, "data", None)},
                            status=status.HTTP_403_FORBIDDEN)

        logger.info("Token validation successful")


        user_info_url = "https://id.vk.com/oauth2/user_info"
        user_info_payload = {"access_token": access_token, "client_id": os.getenv("CLIENT_ID")}

        logger.info("Requesting user info from VK")
        try:
            user_info_response = requests.post(user_info_url, data=user_info_payload, timeout=5)
        except requests.RequestException as e:
            logger.error("Failed to fetch user info", exc_info=True)
            return Response({"error": "Failed to fetch user info"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if user_info_response.status_code != 200:
            logger.error(f"User info endpoint returned {user_info_response.status_code}: {user_info_response.text}")
            return Response(user_info_response.json(), status=user_info_response.status_code)

        vk_user = user_info_response.json()
        vk_id = vk_user.get("sub") or vk_user.get("id")
        logger.info(f"User info received, VK ID: {vk_id}")

        username = f"vk_{vk_id}" if vk_id else None
        email = vk_user.get("email") or f"{vk_id}@vk.local"


        try:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": vk_user.get("first_name", ""),
                    "last_name": vk_user.get("last_name", ""),
                    "email": email,
                },
            )
            if created:
                logger.info(f"New user created: id={user.id}, vk_id={vk_id}")
            else:
                logger.info(f"Existing user updated: id={user.id}, vk_id={vk_id}")
        except Exception as e:
            logger.error("Failed to create/update user", exc_info=True)
            return Response({"error": "user_creation_failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        refresh = RefreshToken.for_user(user)
        access_token_jwt = str(refresh.access_token)
        refresh_token_jwt = str(refresh)
        logger.info(f"JWT tokens generated for user {user.id}")

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


        try:
            access_lifetime = jwt_settings.ACCESS_TOKEN_LIFETIME
            refresh_lifetime = jwt_settings.REFRESH_TOKEN_LIFETIME
            access_max_age = int(access_lifetime.total_seconds())
            refresh_max_age = int(refresh_lifetime.total_seconds())
        except Exception:
            access_max_age = 3600
            refresh_max_age = 60 * 60 * 24 * 7
            logger.warning("Failed to get JWT lifetimes, using defaults")

        secure_flag = not getattr(settings, "DEBUG", False)


        resp.set_cookie("jwt_access", access_token_jwt, httponly=True, secure=secure_flag,
                        samesite="Lax", max_age=access_max_age, path="/")
        resp.set_cookie("jwt_refresh", refresh_token_jwt, httponly=True, secure=secure_flag,
                        samesite="Lax", max_age=refresh_max_age, path="/")
        resp.set_cookie("vk_access", access_token, httponly=True, secure=secure_flag,
                        samesite="Lax", max_age=int(tokens.get("expires_in", access_max_age)), path="/")
        if refresh_token_vk:
            resp.set_cookie("vk_refresh", refresh_token_vk, httponly=True, secure=secure_flag,
                            samesite="Lax", max_age=int(tokens.get("expires_in", refresh_max_age)), path="/")

        logger.info(f"Cookies set for user {user.id}")


        try:
            vk_ttl = tokens.get("expires_in") or access_max_age
            cache.set(f"vk_tokens:{vk_id}", tokens, timeout=int(vk_ttl))
            cache.set(f"jwt_tokens:{user.id}", {"access": access_token_jwt, "refresh": refresh_token_jwt},
                      timeout=refresh_max_age)
            logger.info(f"Tokens cached for user {user.id}")
        except Exception as e:
            logger.warning(f"Failed to cache tokens: {e}", exc_info=True)


        duration = time.time() - start_time
        logger.info(f"VK OAuth successful for user {user.id}, total time: {duration:.2f}s")

        return resp