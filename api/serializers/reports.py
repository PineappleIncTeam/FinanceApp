from rest_framework import serializers


class BudgetSerializer(serializers.Serializer):
    total_budget = serializers.DecimalField(max_digits=19, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=19, decimal_places=2)
    total_income = serializers.DecimalField(max_digits=19, decimal_places=2)
    total_savings = serializers.DecimalField(max_digits=19, decimal_places=2)


class BudgetQueryParamsSerializer(serializers.Serializer):
    date = serializers.DateField(
        required=False,
        help_text="Дата, на которую нужно рассчитать показатели. Формат: YYYY-MM-DD. Если не указана, будет использована текущая дата."
    )
