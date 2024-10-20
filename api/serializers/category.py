import logging
from typing import Any, Dict

from rest_framework import serializers

from api.business_logic import get_user_categories
from api.models import Category
from api.serializers.errors import (CategoryAlreadyExistError,
                                    InvalidCategoryTypeError)

logger = logging.getLogger(__name__)


class CategoriesSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    is_income = serializers.BooleanField()
    is_outcome = serializers.BooleanField()

    def create(self, validated_data: Dict[str, Any]) -> Category:
        category_type = (
            "income" if validated_data.get("is_income") else "outcome")

        if self.is_category_exist(
            name=validated_data["name"],
            category_type=category_type
        ):
            logger.error(
                f"The user [ID: {self.context.get('request').user.pk}, "
                f"name: {self.context.get('request').user.email}] "
                f"can not add category {validated_data['name']} because "
                f"such category is already exist in database."
            )
            raise CategoryAlreadyExistError(
                f"Category {validated_data['name']} "
                f"is already exist in database."
            )

        if (
            validated_data["is_income"] and validated_data["is_outcome"]
        ) or (
            not validated_data["is_income"] and not validated_data["is_outcome"]
        ):
            logger.error(
                f"The user [ID: {self.context.get('request').user.pk}, "
                f"name: {self.context.get('request').user.email}] "
                f"can not define a category {validated_data['name']} "
                f"as both types (income, outcome) at the same time or can not "
                f"add a category without type (both of types is False)."
            )
            raise InvalidCategoryTypeError(
                f"Can not define a category {validated_data['name']} "
                f"as both types (income, outcome) at the same time or can not "
                f"add a category without type (both of types is False)."
            )

        validated_data["user"] = self.context.get("request").user

        logger.info(
            f"The user [ID: {self.context.get('request').user.pk}, "
            f"name: {self.context.get('request').user.email}] "
            f"successfully added a new category."
        )
        return super().create(validated_data)

    def is_category_exist(self, name: str, category_type: str) -> bool:
        all_user_categories = get_user_categories(
            user=self.context.get("request").user,
            category_type=category_type
        )

        for category in all_user_categories:
            if category["name"].lower() == name.lower():
                return True
        return False

    class Meta:
        model = Category
        fields = ['id', 'name', "is_income", "is_outcome", 'is_deleted']
