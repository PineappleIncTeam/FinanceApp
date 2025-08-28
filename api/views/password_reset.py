from __future__ import annotations

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer, CharField
from rest_framework.request import Request

from api.models import User


class TokenInvalidException(APIException):
    status_code = 407
    default_detail = "Token is invalid or expired."
    default_code = "token_invalid"


class PasswordResetConfirmQuerySerializer(Serializer):
    uid = CharField(required=True)
    token = CharField(required=True)

class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmQuerySerializer

    @swagger_auto_schema(
        operation_id="Подтверждение восстановления пароля",
        operation_description="Подтверждение восстановления пароля",
        responses={200: "OK"}
    )
    def get(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise TokenInvalidException()

        if not default_token_generator.check_token(user, token):
            raise TokenInvalidException()

        return Response(data={"detail": "Token is valid"}, status=status.HTTP_200_OK)

