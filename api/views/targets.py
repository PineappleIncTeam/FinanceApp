from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (DestroyAPIView, ListCreateAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from api.models import IN_PROGRESS
from api.serializers import TargetsSerializer
from api.utils import get_user_targets, return_money_from_target_to_incomes

from .errors import TargetInProgressError, TargetIsClosedError
from ..serializers.profile import ErrorSerializer

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


    @swagger_auto_schema(
        operation_id='Получение профиля пользователя',
        operation_description='получение профиля пользователя',
    responses = {
        200: openapi.Response(description="Профиль успешно получен", schema=TargetsSerializer),
        401: openapi.Response(description="Неавторизованный запрос", schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
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
