from __future__ import annotations

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.request import Request

from api.models import User


class TokenInvalidException(APIException):
    status_code = 403
    default_detail = "Неверный токен или пользователь не найден."
    default_code = "token_invalid"


class PasswordResetConfirmQuerySerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    re_new_password = serializers.CharField(required=True)


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmQuerySerializer

    @swagger_auto_schema(
        operation_id="Подтверждение восстановления пароля",
        operation_description="Подтверждение восстановления пароля",
        request_body=PasswordResetConfirmQuerySerializer,
        responses={
            200: "Token is valid",
            403: "Token is invalid or expired"
        }
    )
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]
        re_new_password = serializer.validated_data["re_new_password"]

        if new_password != re_new_password:
            return Response(
                {"detail": "Пароли не совпадают."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise TokenInvalidException()

        if not default_token_generator.check_token(user, token):
            raise TokenInvalidException()

        user.set_password(new_password)
        user.save()

        return Response(data={"detail": "Пароль успешно изменён"}, status=status.HTTP_200_OK)





