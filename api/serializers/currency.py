from rest_framework import serializers

from api.models import CurrencyData


class CurrencyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyData
        fields = ["currency", "rate"]
