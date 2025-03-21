import logging
from typing import Any, Dict

from rest_framework import serializers

from api.models import Category
from api.serializers.errors import CategoryExistsError
from api.utils import get_user_categories

logger = logging.getLogger(__name__)


class CategoriesSerializer(serializers.ModelSerializer):

    def create(self, validated_data: Dict[str, Any]) -> Category:
        """
        Create category instance if category does not exist
        or retrieve it from archive.
        """

        validated_data["user"] = self.context.get("request").user

        all_categories = get_user_categories(
            user=self.context.get("request").user,
            is_income=validated_data.get("is_income"),
            is_outcome=validated_data.get("is_outcome"),
        )

        for category in all_categories:
            if category.name.lower() == validated_data["name"].lower():
                if category.is_deleted:
                    category.is_deleted = False
                    category.save()
                    logger.info(
                        f"The user [ID: {self.context.get('request').user.pk},"
                        f" name: {self.context.get('request').user.email}] "
                        f"has retrieved a category {validated_data['name']} "
                        f"from the archive."
                    )
                    return category

                else:
                    logger.error(
                        f"The user [ID: {self.context.get('request').user.pk},"
                        f" name: {self.context.get('request').user.email}] "
                        f"can not add a new category {validated_data['name']} "
                        f"because of category existance."
                    )

                    raise CategoryExistsError()

        logger.info(
            f"The user [ID: {self.context.get('request').user.pk}, "
            f"name: {self.context.get('request').user.email}] "
            f"successfully added a new category {validated_data['name']}."
        )
        return super().create(validated_data)

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check correct category type usage.
        """

        if (data["is_income"] and data["is_outcome"]) or (
            not data["is_income"] and not data["is_outcome"]
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

        return data

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "is_income",
            "is_outcome",
            "is_visibility",
            "is_deleted",
        ]
        read_only_fields = ["is_deleted"]

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            if not instance.is_visibility:
                return {}
            return representation


class CategoriesGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "is_income",
            "is_outcome",
            "is_visibility",
            "is_system",
            "is_deleted",
        ]
        read_only_fields = ["is_deleted"]

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["is_deleted"]

