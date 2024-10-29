from rest_framework import serializers


class BalanceSerializer(serializers.Serializer):
    current_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
