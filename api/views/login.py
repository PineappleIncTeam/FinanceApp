import requests
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.http import JsonResponse
from rest_framework.permissions import AllowAny

from api.models import User
from api.serializers import LoginSerializer
from api.serializers.profile import ErrorSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_id="Авторизация",
        operation_description="Авторизация пользователя",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(description="Успешная авторизация"),
            401: openapi.Response(description="Ошибка авторизации"),
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"error": "User account is not active"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        response = JsonResponse({"access": access})
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=7 * 24 * 60 * 60,
        )
        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=5 * 60,
        )
        return response


class TokenRefreshView(GenericAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="Обновление токена",
        operation_description="Обновление токена",
        responses={
            200: openapi.Response(description="Новый access-токен успешно выдан"),
            500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
            401: openapi.Response(description="Ошибка токена", schema=ErrorSerializer),
        },
    )
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response({"error": "Нет refresh-токена в cookies"}, status=status.HTTP_401_UNAUTHORIZED)

        if refresh_token.startswith("vk2"):
            vk_check = self._check_vk_token(refresh_token, request)
            return vk_check

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({"access": access_token}, status=status.HTTP_200_OK)
            response.set_cookie(
                key="access_token", value=access_token, httponly=True, secure=True, samesite="Strict", max_age=5 * 60
            )
            return response

        except TokenError:
            raise AuthenticationFailed("Недействительный или просроченный refresh-токен")


class TokenVerifyView(GenericAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="Проверка токена",
        operation_description="Проверка валидности access-токена из cookies",
        responses={
            200: openapi.Response(description="Токен валиден"),
            401: openapi.Response(description="Недействительный токен", schema=ErrorSerializer),
        },
    )
    def get(self, request):
        access_token = request.COOKIES.get("access_token")

        if not access_token:
            return Response({"error": "Access-токен отсутствует в cookies"}, status=status.HTTP_401_UNAUTHORIZED)

        if access_token.startswith("vk2"):
            vk_check = self._check_vk_token(access_token, request)
            return vk_check

        try:
            AccessToken(access_token)
            return Response({"detail": "Access-токен валиден"}, status=status.HTTP_200_OK)

        except (TokenError, InvalidToken):
            return Response(
                {"error": "Недействительный или просроченный access-токен"}, status=status.HTTP_401_UNAUTHORIZED
            )

    def _check_vk_token(self, token, request):
        """
        Выполняет обращение к VK API secure.checkToken и возвращает Response
        Поведение соответствует логике из VKCheckTokenView.post
        """
        params = {"token": token, "access_token": settings.VK_SERVICE_KEY, "v": "5.131"}

        ip = request.query_params.get("ip") or request.META.get("REMOTE_ADDR")
        if ip:
            params["ip"] = ip

        try:
            vk_response = requests.get("https://api.vk.com/method/secure.checkToken", params=params, timeout=5)
        except requests.RequestException:
            return Response(
                {"error": "server_error", "error_description": "Не удалось связаться с VK API"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            data = vk_response.json()
        except ValueError:
            return Response(
                {"error": "server_error", "error_description": "Неверный ответ от VK API"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if "response" in data:
            return Response(data["response"], status=status.HTTP_200_OK)
        else:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
