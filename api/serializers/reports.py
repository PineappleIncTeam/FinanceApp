from rest_framework import serializers


class BudgetSerializer(serializers.Serializer):
    total_budget = serializers.DecimalField(max_digits=19, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=19, decimal_places=2)
    total_income = serializers.DecimalField(max_digits=19, decimal_places=2)
    total_savings = serializers.DecimalField(max_digits=19, decimal_places=2)


class MonthSumSerializer(serializers.Serializer):
    month = serializers.CharField()
    amount = serializers.DecimalField(max_digits=19, decimal_places=2)


class CategoryAggregationSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    category_name = serializers.CharField()
    month_sums = MonthSumSerializer(many=True)
