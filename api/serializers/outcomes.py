from rest_framework import serializers

from api.models import Outcomes


class OutcomeSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """
        Return a dict of object params.
        """

        item = {
            "id": instance.get("id"),
            "sum": instance.get("sum"),
            "category": instance.get("category__name"),
            "created_at": instance.get("created_at"),
        }
        return item

    class Meta:
        model = Outcomes
        fields = ["id", "sum", "category", "created_at"]
        depth = 2
