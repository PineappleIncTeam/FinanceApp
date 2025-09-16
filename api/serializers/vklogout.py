from rest_framework import serializers

class LogoutResponseSerializer(serializers.Serializer):
    response = serializers.IntegerField(help_text="0 или 1")
