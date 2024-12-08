from rest_framework import serializers


class BalanceSerializer(serializers.Serializer):
    current_balance = serializers.DecimalField(max_digits=19, decimal_places=2)


class StatisticsSerializer(serializers.Serializer):
    total_expenses = serializers.DecimalField(max_digits=19, decimal_places=2)
    total_income = serializers.DecimalField(max_digits=19, decimal_places=2)
    total_savings = serializers.DecimalField(max_digits=19, decimal_places=2)


class MonthSumSerializer(serializers.Serializer):
    month = serializers.CharField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)


class ReportCategorySerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    category_name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)
    items = MonthSumSerializer(many=True)
