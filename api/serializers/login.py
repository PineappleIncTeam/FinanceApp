from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)


class TokenVerifySerializer(serializers.Serializer):
    access_token = serializers.CharField()