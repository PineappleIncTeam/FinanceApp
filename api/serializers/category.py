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
                        "The user [ID: %s,"
                        " name: %s "
                        "has retrieved a category %s "
                        "from the archive.",
                        self.context.get('request').user.pk,
                        self.context.get('request').user.name,
                        validated_data['name']
                    )
                    return category

                else:
                    logger.error(
                        "The user [ID: %s,"
                        " name: %s] "
                        "can not add a new category %s "
                        "because of category existance.",
                        self.context.get('request').user.pk,
                        self.context.get('request').user.name,
                        validated_data['name']

                    )



                    raise CategoryExistsError()

        logger.info(
            "The user [ID: %s, "
            "name: %s] "
            "successfully added a new category %s.",
            self.context.get('request').user.pk,
            self.context.get('request').user.name,
            validated_data['name']
        )
        return super().create(validated_data)

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check correct category type usage.
        """
        s_sym = "!@#$%^&*()+={}[]|\:;'<>,.?/~`_"
        if len(data["name"]) > 14:
            raise serializers.ValidationError(
                f"the name is too long, max 14 characters (you entered {len(data['name'])})")
        if (data["is_income"] and data["is_outcome"]) or (
            not data["is_income"] and not data["is_outcome"]
        ):
            logger.error(
                "The user [ID: %s, "
                "name: %s] "
                "can not define a category %s "
                "as both types (income, outcome) at the same time or can not "
                "add a category without type (both of types is False).",
                self.context.get('request').user.pk,
                self.context.get('request').user.name,
                data['name']
            )
            raise serializers.ValidationError(
                "Invalid category type (the same data for fields "
                "is_income and is_outcome.)"
            )
        for i in data["name"]:
            if i in s_sym:
                raise serializers.ValidationError(
                    "You can't use special characters in the name.")

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

