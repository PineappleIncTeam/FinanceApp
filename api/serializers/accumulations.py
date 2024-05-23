import logging
import traceback
from typing import Any, Dict, Union

from django.db.models import Sum
from rest_framework import serializers

from api.business_logic.errors import (MissingTargetError,
                                       TargetExceedingError,
                                       TargetHasReachedError)
from api.models import Accumulations, Targets

logger = logging.getLogger(__name__)


class AcumulationCategoriesSerializer(serializers.ModelSerializer):

    def create(self, validated_data: Dict[str, Any]) -> Targets:
        """
        Create a new Target instance.
        """

        user = self.context.get("request").user
        validated_data["user"] = user

        try:
            instance = Targets.objects.create(**validated_data)
            logger.info(
                f"The user [ID: {user.pk}, "
                f"name: {user.email}] "
                f"successfully created a new Targets instance."
            )
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    Targets.__name__,
                    Targets._default_manager.name,
                    Targets.__name__,
                    Targets._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)
        return instance

    class Meta:
        model = Targets
        fields = ["id", "target_name", "target_sum"]


class AccumulationSerializer(serializers.ModelSerializer):

    def to_representation(self, instance: Accumulations) -> Dict[str, Any]:
        """
        Return a dict of object params.
        """

        item = {
            "id": instance.id,
            "sum": instance.sum,
            "target": instance.target.target_name,
            "created_at": instance.created_at
        }
        return item

    class Meta:
        model = Accumulations
        fields = ['sum', 'target', 'created_at']


class AccumulationCreateSerializer(serializers.ModelSerializer):
    """
    To create an accumulation instance.
    """

    def create(self, validated_data: Dict[str, Union[Targets, float]]) -> Accumulations:
        target = validated_data.get("target")
        sum_data = validated_data.get("sum")

        if isinstance(target, Targets):
            total_sum = (
                Accumulations.objects
                .filter(target=target.pk)
                .aggregate(total_sum=Sum("sum"))
                .get("total_sum")
            )

            if total_sum == target.target_sum:
                logger.error(
                    f"The user [ID: {self.context.get('request').user.pk}, "
                    f"name: {self.context.get('request').user.email}] "
                    f"can't add a new Accumulations instance because of"
                    f"the target {target.target_name} has already been reached"
                )
                raise TargetHasReachedError(
                    f"The target {target.target_name} has already been reached."
                )

            elif total_sum + sum_data > target.target_sum:
                logger.error(
                    f"The user [ID: {self.context.get('request').user.pk}, "
                    f"name: {self.context.get('request').user.email}] "
                    f"can't add {sum_data} of money because of"
                    f"the accumulation goal will be exceeded."
                )
                raise TargetExceedingError(
                    f"If you add {sum_data} to the target "
                    f"{target.target_name}, you will exceed the accumulation goal."
                    f"You should change the sum: {sum_data}."
                    f"Max amount is {target.target_sum - total_sum}."
                )

            accumulation_instance = Accumulations.objects.create(**validated_data)
            logger.info(
                f"The user [ID: {self.context.get('request').user.pk}, "
                f"name: {self.context.get('request').user.email}] "
                f"successfully added a new Accumulations instance."
            )
            return accumulation_instance

        else:
            raise MissingTargetError("The request hasn't target or sum parameters.")

    class Meta:
        model = Accumulations
        fields = '__all__'


class AccumulationInfoSerializer(serializers.Serializer):
    total_sum = serializers.DecimalField(max_digits=9, decimal_places=2)
    target_sum = serializers.DecimalField(max_digits=9, decimal_places=2)
    target_name = serializers.CharField()


class ArchiveAccumulationCategorySerializer(serializers.Serializer):
    is_hidden = serializers.BooleanField()
