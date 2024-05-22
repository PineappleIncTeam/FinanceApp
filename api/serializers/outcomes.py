from rest_framework import serializers
from typing import Dict, Any
from api.models import Outcomes, OutcomeCategories


class OutcomeSerializer(serializers.ModelSerializer):
    def to_representation(self, instance: Outcomes) -> Dict[str, Any]:
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
        model = Outcomes
        fields = ["sum", "category", "created_at", "is_hidden"]


class OutcomeCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeCategories
        fields = ["id", "name"]

