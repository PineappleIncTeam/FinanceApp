import logging
from typing import Any, Dict

from rest_framework import serializers

from api.models import IncomeCategories, Incomes

logger = logging.getLogger(__name__)


class IncomeCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategories
        fields = ["id", "name"]


class IncomeSerializer(serializers.ModelSerializer):

    def to_representation(self, instance: Incomes) -> Dict[str, Any]:
        """
        Return a dict of object params.
        """

        item = {
            "id": instance.id,
            "sum": instance.sum,
            "category": instance.category.name,
            "created_at": instance.created_at,
            "is_hidden": instance.is_hidden
        }
        return item

    class Meta:
        model = Incomes
        fields = ['sum', 'category', 'created_at', 'is_hidden']


class IncomeCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
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
