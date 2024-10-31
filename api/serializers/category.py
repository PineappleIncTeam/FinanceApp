import logging
from typing import Any, Dict

from rest_framework import serializers

from api.business_logic import get_user_categories
from api.models import Category

logger = logging.getLogger(__name__)


class CategoriesSerializer(serializers.ModelSerializer):
    is_deleted = serializers.BooleanField(required=False)

    def create(self, validated_data: Dict[str, Any]) -> Category:
        validated_data["user"] = self.context.get("request").user

        logger.info(
            f"The user [ID: {self.context.get('request').user.pk}, "
            f"name: {self.context.get('request').user.email}] "
            f"successfully added a new category {validated_data['name']}."
        )
        return super().create(validated_data)

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check correct category type usage.
        Check category existance.
        """

        if (data['is_income'] and data['is_outcome']) or (
            not data['is_income'] and not data['is_outcome']
        ):
            logger.error(
                f"The user [ID: {self.context.get('request').user.pk}, "
                f"name: {self.context.get('request').user.email}] "
                f"can not define a category {data['name']} "
                f"as both types (income, outcome) at the same time or can not "
                f"add a category without type (both of types is False)."
            )
            raise serializers.ValidationError(
                "Invalid category type (the same data for fields "
                "is_income and is_outcome.)"
            )

        all_categories = get_user_categories(
            user=self.context.get('request').user,
            is_income=data.get("is_income"),
            is_outcome=data.get("is_outcome"),
            is_deleted=data.get("is_deleted")
        )

        for category in all_categories:
            if category.name.lower() == data["name"].lower():
                logger.error(
                    f"The user [ID: {self.context.get('request').user.pk}, "
                    f"name: {self.context.get('request').user.email}] can not "
                    f"add a new category {data['name']} "
                    f"because of category existance."
                )

                raise serializers.ValidationError(
                    "The category already exists."
                )

        return data

    class Meta:
        model = Category
        fields = ['id', 'name', "is_income", "is_outcome", 'is_deleted']


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['is_deleted']
