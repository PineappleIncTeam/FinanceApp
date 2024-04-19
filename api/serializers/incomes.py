from rest_framework import serializers
from api.models import IncomeCategories, Incomes


class IncomeCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategories
        fields = ['id', 'name']


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incomes
        fields = ['id', 'sum', 'category', 'created_at']
