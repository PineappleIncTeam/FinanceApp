import os
import logging
import time
import requests
import json
import uuid
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
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        logger.info(f"[{request_id}] VKOAuth2View: request started")

        try:
            code = request.data.get("code")
            code_verifier = request.data.get("code_verifier")
            device_id = request.data.get("device_id")

            logger.info(f"[{request_id}] Received code: {'present' if code else 'missing'}, "
                        f"code_verifier: {'present' if code_verifier else 'missing'}, "
                        f"device_id: {device_id}")

            if not code or not code_verifier or not device_id:
                missing = [k for k, v in [('code', code), ('code_verifier', code_verifier), ('device_id', device_id)] if not v]
                logger.warning(f"[{request_id}] Missing parameters: {missing}")
                logger.info(f"[{request_id}] Returning 400: Missing parameters")
                return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"[{request_id}] All required parameters present")


            redirect_uri = os.getenv("REDIRECT_URI")
            if not redirect_uri:
                redirect_uri = "https://dev.freenance.space/api/v1/vkauth/"
                logger.warning(f"[{request_id}] REDIRECT_URI not set, using default: {redirect_uri}")

            vk_token_url = "https://id.vk.com/oauth2/auth"
            payload = {
                "grant_type": "authorization_code",
                "code": code,
                "code_verifier": code_verifier,
                "device_id": device_id,
                "client_id": os.getenv("CLIENT_ID"),
                "client_secret": os.getenv("CL_SECRET"),
                "redirect_uri": redirect_uri,
            }


            logger.info(f"[{request_id}] VK token request params: "
                        f"grant_type={payload['grant_type']}, "
                        f"redirect_uri={payload['redirect_uri']}, "
                        f"client_id={payload['client_id']}, "
                        f"code_verifier_length={len(code_verifier) if code_verifier else 0}, "
                        f"code_verifier_prefix={code_verifier[:5] if code_verifier and len(code_verifier) > 5 else code_verifier}")

            logger.info(f"[{request_id}] Requesting VK token endpoint (code exchange)")
            start_vk = time.time()
            try:
                vk_response = requests.post(vk_token_url, data=payload, timeout=5)
            except requests.RequestException as e:
                logger.error(f"[{request_id}] Failed to reach VK token endpoint", exc_info=True)
                logger.info(f"[{request_id}] Returning 500: VK token endpoint unreachable")
                return Response({"error": "Failed to reach VK token endpoint"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            vk_duration = time.time() - start_vk
            logger.info(f"[{request_id}] VK token request took {vk_duration:.2f}s")

            if vk_response.status_code != 200:
                logger.error(f"[{request_id}] VK token endpoint returned {vk_response.status_code}: {vk_response.text}")
                logger.info(f"[{request_id}] Returning {vk_response.status_code} from VK")
                return Response(vk_response.json(), status=vk_response.status_code)

            try:
                tokens = vk_response.json()
            except ValueError as e:
                logger.error(f"[{request_id}] Failed to parse VK response JSON: {vk_response.text}", exc_info=True)
                logger.info(f"[{request_id}] Returning 500: Invalid JSON from VK")
                return Response({"error": "Invalid JSON from VK"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            access_token = tokens.get("access_token")
            refresh_token_vk = tokens.get("refresh_token")

            logger.info(f"[{request_id}] Using redirect_uri: {payload.get('redirect_uri')}")

            if not access_token:
                logger.error(f"[{request_id}] No access_token in VK response. Full response: {json.dumps(tokens, separators=(',', ':'))}")
                logger.info(f"[{request_id}] Returning 403: No access token")
                return Response({"error": "No access token received"}, status=status.HTTP_403_FORBIDDEN)

            if refresh_token_vk:
                logger.info(f"[{request_id}] VK refresh token received")
            else:
                logger.info(f"[{request_id}] No VK refresh token")


        except Exception as e:
            logger.exception(f"[{request_id}] Unhandled exception in VKOAuth2View")
            logger.info(f"[{request_id}] Returning 500 due to unhandled exception")
            return Response({"error": "internal_server_error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)