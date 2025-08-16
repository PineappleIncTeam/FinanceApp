from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework.permissions import AllowAny

from api.serializers import LoginSerializer
from api.serializers.profile import ErrorSerializer


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="Авторизация",
        operation_description="Авторизация пользователя",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(description="Успешная авторизация"),
            401: openapi.Response(description="Ошибка авторизации"),
        }
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Неверный пароль'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        response = JsonResponse({'access': access})
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=7 * 24 * 60 * 60
        )
        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=5 * 60
        )
        return response


class TokenRefreshView(GenericAPIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_id='Обновление токена',
        operation_description='Обновление токена',
        responses={
            200: openapi.Response(description="Новый access-токен успешно выдан"),
            500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
            401: openapi.Response(description="Ошибка токена", schema=ErrorSerializer),
        }
    )
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response({'error': 'Нет refresh-токена в cookies'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({'access': access_token}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=5 * 60
            )
            return response

        except TokenError:
            raise AuthenticationFailed('Недействительный или просроченный refresh-токен')
