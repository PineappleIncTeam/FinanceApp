from rest_framework import serializers

from api.models import Category, Operation, Target


class OperationSerializer(serializers.ModelSerializer):

    def validate_amount(self, value):
        """
        Validate that the operation amount is not negative.
        """
        if value < 0:
            raise serializers.ValidationError("Operation amount cannot be negative.")
        return value

    def validate_categories(self, value):
        """
        Validate the category field.
        """
        if value and not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Category does not exist.")
        return value

    def validate_target(self, value):
        """
        Validate the target field.
        """
        if value and not Target.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Target does not exist.")
        return value

    def validate(self, data):
        """
        Object-level validation to ensure category and target constraints.
        """
        type_operation = data.get("type")
        category = data.get("categories")
        target = data.get("target")

        if category and target:
            raise serializers.ValidationError(
                "Category and target cannot be both specified."
            )

        if not category and not target:
            raise serializers.ValidationError(
                "Either category or target must be specified."
            )

        if category:
            if type_operation == "income" and not category.is_income:
                raise serializers.ValidationError(
                    "Category must be an income category for income operations."
                )
            if type_operation == "outcome" and not category.is_outcome:
                raise serializers.ValidationError(
                    "Category must be an outcome category for outcome operations."
                )
            if type_operation == "targets" and any(
                (category.is_outcome, category.is_income)
            ):
                raise serializers.ValidationError(
                    "Category type can't be outcome or income for targets operations."
                )

        if target:
            if type_operation != "targets":
                raise serializers.ValidationError(
                    "Targets operations can't be specified as incomes or outcomes."
                )

        return data

    class Meta:
        model = Operation
        fields = ['id', 'type', 'amount', 'date', 'categories', 'target']


class OperationInfoSerializer(serializers.ModelSerializer):
    def validate_amount(self, value):
        """
        Validate that the operation amount is not negative.
        """
        if value < 0:
            raise serializers.ValidationError("Operation amount cannot be negative.")
        return value

    class Meta:
        model = Operation
        fields = ['id', 'amount', 'date', 'categories', 'target']
        read_only_fields = ['categories', 'target']
