from rest_framework import serializers

class LogoutRequestSerializer(serializers.Serializer):
    client_id = serializers.CharField(help_text="Идентификатор приложения")
    access_token = serializers.CharField(help_text="Access token пользователя")

    class Meta:
        ref_name = "VKLogoutRequest"


class LogoutResponseSerializer(serializers.Serializer):
    response = serializers.IntegerField(help_text="0 или 1")

    class Meta:
        ref_name = "VKLogoutResponse"
