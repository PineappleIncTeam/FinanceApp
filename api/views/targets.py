from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (DestroyAPIView, ListCreateAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from api.models import IN_PROGRESS
from api.serializers import TargetsSerializer
from api.utils import get_user_targets, return_money_from_target_to_incomes

from .errors import TargetInProgressError, TargetIsClosedError

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from api.models import Target


logger = logging.getLogger(__name__)


class TargetsListCreateAPI(ListCreateAPIView):
    """
    получение списка накоплений пользователя и создание новой цели
    """

    serializer_class = TargetsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_deleted']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Target]:
        return get_user_targets(
            user=self.request.user
        )


class TargetUpdateDestroyAPI(UpdateAPIView, DestroyAPIView):
    """
    закрытие цели. изменение названия или суммы
    """

    serializer_class = TargetsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Target]:
        return get_user_targets(
            user=self.request.user
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        instance: Target = self.get_object()
        if instance.is_deleted:
            raise TargetIsClosedError()
        if instance.status == IN_PROGRESS:
            raise TargetInProgressError()
        try:
            returned_operation = return_money_from_target_to_incomes(
                user=request.user,
                target=instance
            )
            instance.is_deleted = True
            instance.current_sum = 0
            instance.save()
        except IntegrityError:
            return Response(
                "Can not return money from a target to incomes.",
                status=HTTP_400_BAD_REQUEST
            )

        logger.info(
            f"The user [ID: {request.user.pk}, "
            f"name: {request.user.email}] closed a target: "
            f"id {instance.id}, name - {instance.name},"
            f"returned amount - {returned_operation.amount}."
        )

        return Response(
            data=TargetsSerializer(instance).data,
            status=HTTP_200_OK
        )


class TargetMoneyReturnAPI(DestroyAPIView):
    """
    возврат цели в доходы
    """
    serializer_class = TargetsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Target]:
        return get_user_targets(
            user=self.request.user
        )
