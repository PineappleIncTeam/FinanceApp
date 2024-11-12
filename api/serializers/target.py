import logging
from typing import Any, Dict

from rest_framework import serializers

from api.models import Target

logger = logging.getLogger(__name__)


class TargetsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=14)

    def create(self, validated_data: Dict[str, Any]) -> Target:
        """
        Create target instance if category does not exist
        or retrieve it from archive.
        """

        validated_data["user"] = self.context.get("request").user

        logger.info(
            f"The user [ID: {self.context.get('request').user.pk}, "
            f"name: {self.context.get('request').user.email}] "
            f"successfully added a new category {validated_data['name']}."
        )
        return super().create(validated_data)

    def validate_amount(self, value: float) -> float:
        """
        Check that amount is positive number.
        """

        if value < 0:
            logger.error(
                f"The user [ID: {self.context.get('request').user.pk}, "
                f"name: {self.context.get('request').user.email}] "
                f"can not add a target that is a negative number."
            )
            raise serializers.ValidationError(
                "A target amount cannot be negative.")
        return value

    class Meta:
        model = Target
        fields = ['id', 'name', 'amount']
        read_only_fields = ['is_deleted', 'status']
