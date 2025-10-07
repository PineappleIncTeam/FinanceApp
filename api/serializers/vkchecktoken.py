from rest_framework import serializers


class VKCheckTokenRequestSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Access token пользователя")
    ip = serializers.CharField(help_text="IP-адрес пользователя (опционально)", required=False)

    class Meta:
        ref_name = "VKCheckTokenRequest"


class VKCheckTokenResponseSerializer(serializers.Serializer):
    success = serializers.IntegerField()
    user_id = serializers.IntegerField()
    date = serializers.IntegerField()
    expire = serializers.IntegerField()

    class Meta:
        ref_name = "VKCheckTokenResponse"
