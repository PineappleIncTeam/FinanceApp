import logging
from typing import Any

from rest_framework import serializers

from api.models import IncomeCategories, Incomes

logger = logging.getLogger(__name__)


class IncomeCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategories
        fields = ["id", "name"]


class IncomeSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        """
        Return a dict of object params.
        """

        item = {
            "id": instance.get('id'),
            "sum": instance.get('sum'),
            "category": instance.get('category__name'),
            "created_at": instance.get('created_at')
        }
        return item

    class Meta:
        model = Incomes
        fields = ['id', 'sum', 'category', 'created_at']
        depth = 2


class IncomeCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict[str, Any]) -> Incomes:
        validated_data["user"] = self.context.get("request").user
        logger.info(
            f"The user [ID: {self.context.get('request').user.pk}, "
            f"name: {self.context.get('request').user.email}] "
            f"successfully added a new Incomes instance."
        )
        return super().create(validated_data)

    class Meta:
        model = Incomes
        fields = ["id", "sum", "category", "created_at"]
