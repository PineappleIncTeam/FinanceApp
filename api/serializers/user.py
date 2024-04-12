from django.contrib.auth import get_user_model, authenticate
from djoser.serializers import TokenCreateSerializer, UserCreatePasswordRetypeSerializer
from django.utils.html import escape

from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.settings import api_settings
from api.validators import validate_user_email


class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs) -> None:
        password = attrs.get("password")
        params = {get_user_model().USERNAME_FIELD: attrs.get(get_user_model().USERNAME_FIELD)}
        self.user = authenticate(
            **params, password=escape(password)
        )

        if not self.user:
            self.user = get_user_model().objects.filter(**params).first()
            if self.user and not self.user.check_password(escape(password)):
                self.fail("invalid_credentials")
        if self.user and self.user.is_active:
            return attrs
        self.fail("invalid_credentials")


class CustomUserCreateSerializer(UserCreatePasswordRetypeSerializer):
    def validate_email(self, value):
        try:
            validate_user_email(email=value)
        except ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"email": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        return value
