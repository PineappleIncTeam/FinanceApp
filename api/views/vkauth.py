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
                "code": openapi.Schema(type=openapi.TYPE_STRING),
                "code_verifier": openapi.Schema(type=openapi.TYPE_STRING),
                "device_id": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(
                description="Успешный ответ (токены в куки)",
                examples={
                    "application/json": {
                        "id_token": "id_token_example",
                        "user_info": {
                            "user_id": "1234567890",
                            "first_name": "Ivan",
                            "last_name": "Ivanov",
                            "avatar": "...",
                            "sex": 2,
                            "verified": False,
                            "birthday": "01.01.2000",
                        },
                    }
                },
            ),
            400: openapi.Response(description="Неверные параметры запроса"),
            500: openapi.Response(description="Ошибка сервера"),
        },
    )
    def post(self, request):
        code = request.data.get("code")
        verifier = request.data.get("code_verifier")
        device = request.data.get("device_id")

        if not all([code, verifier, device]):
            return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

        token_resp = requests.post(
            "https://id.vk.com/oauth2/auth",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "code_verifier": verifier,
                "device_id": device,
                "client_id": os.getenv("CLIENT_ID"),
                "client_secret": os.getenv("CL_SECRET"),
                "redirect_uri": os.getenv("REDIRECT_URI"),
            },
        )

        if token_resp.status_code != 200:
            return Response({"error": "Failed to exchange code"}, status=token_resp.status_code)

        tokens = token_resp.json()
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        id_token = tokens.get("id_token")

        if not access_token or not refresh_token:
            return Response({"error": "No tokens received"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user_resp = requests.post(
            "https://id.vk.com/oauth2/user_info",
            data={"access_token": access_token, "client_id": os.getenv("CLIENT_ID")},
        )

        if user_resp.status_code != 200:
            return Response({"error": "Failed to fetch user info"}, status=user_resp.status_code)

        user_info = user_resp.json()

        resp = Response({"id_token": id_token, "user_info": user_info}, status=status.HTTP_200_OK)

        resp.set_cookie(
            key="access_token", value=access_token, httponly=True, secure=True, samesite="Strict", max_age=3600  # 1 час
        )
        resp.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=60 * 60 * 24 * 30,  # 30 дней
        )

        return resp
