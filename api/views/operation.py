from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.exceptions import NotFound
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView, GenericAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import ACHIEVED, IN_PROGRESS, TARGETS, Operation, Target
from api.serializers import OperationInfoSerializer, OperationSerializer
from FinanceBackend.settings import MAX_OPERATIONS_COUNT

from .errors import (ExceedingTargetAmountError,
                     InvalidTargetOperationDateError,
                     ReturnMoneyCategoryOperationError, TargetArchievedError,
                     TargetIsClosedError)
from ..serializers.profile import ErrorSerializer, ProfileSerializer


class OperationListCreateAPI(GenericAPIView):

    serializer_class = OperationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [BaseFilterBackend]
    filter_fields = ["type"]

    def get_queryset(self):
        return Operation.objects.filter(user=self.request.user)


    @swagger_auto_schema(
        operation_id='Получение списка операций',
        operation_description='Получение списка всех операций',
    responses = {
        200: openapi.Response(description="Операции успешно получены", schema=OperationSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        operation_type = request.query_params.get("type", None)
        if operation_type:
            if operation_type == "TARGETS":
                queryset = queryset.filter(type=operation_type, categories=None)
            else:
                queryset = queryset.filter(type=operation_type)

        last_five = request.query_params.get("last_five", "true")
        if last_five.lower() == "true":
            queryset = queryset.order_by("-date", "-id")[:MAX_OPERATIONS_COUNT]
        else:
            queryset = queryset.order_by("-date", "-id")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @swagger_auto_schema(
        operation_id='Создание операции',
        operation_description='Создание операции',
    responses = {
        200: openapi.Response(description="Операции успешно создана", schema=OperationSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if request.data["type"] == TARGETS:
                target = Target.objects.get(id=request.data["target"])
                current_sum = target.current_sum + Decimal(request.data["amount"])
                if target.status == ACHIEVED:
                    raise TargetArchievedError()
                elif target.is_deleted:
                    raise TargetIsClosedError()
                elif current_sum > target.amount:
                    raise ExceedingTargetAmountError()
                elif datetime.strptime(
                        request.data["date"], "%Y-%m-%d"
                ).date() < target.created_at.date():
                    raise InvalidTargetOperationDateError()
                elif current_sum == target.amount:
                    target.status = ACHIEVED
                target.current_sum = current_sum
                target.save()
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OperationRetrieveUpdateDestroyAPI(GenericAPIView):
    """
    Удаление, обновление и частичное обновление операции по ее уникальному идентификатору.
    """
    serializer_class = OperationInfoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        """
        Получить список операций текущего пользователя.
        """
        return Operation.objects.filter(user=self.request.user)


    @swagger_auto_schema(
        operation_id='Получить операцию',
        operation_description='Получить операцию по уникальному идентификатору',
        responses = {
        200: openapi.Response(description="Операция успешно получена ", schema=OperationInfoSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def get(self, request, *args, **kwargs):
        operation = self.get_object()  # Получаем операцию с помощью метода get_object
        serializer = self.get_serializer(operation)  # Сериализуем операцию
        return Response(serializer.data, status=status.HTTP_200_OK)  # Возвращаем сериализованные данные операции


    @swagger_auto_schema(
        operation_id='Удаление операции',
        operation_description='Удаление операции, если операция связана с установленной целью то деньги возвращаются',
        responses={
        200: openapi.Response(description="Операция успешно удалена", schema=OperationInfoSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def delete(self, request, *args, **kwargs):
        operation_instance: Operation = self.get_object()

        if operation_instance.type == "TARGETS":
            if operation_instance.categories:
                raise ReturnMoneyCategoryOperationError()

            target_instance = Target.objects.get(id=operation_instance.target.pk)
            target_instance.current_sum -= operation_instance.amount
            target_instance.status = "IN_PROGRESS"
            target_instance.save()

        operation_instance.delete()

        return Response({"detail": "Запись успешна удалена"},status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_id='Изменение операции',
        operation_description='Изменение операции',
        responses={
        200: openapi.Response(description="Операция успешно изменена", schema=OperationInfoSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def patch(self, request, *args, **kwargs):
        operation_instance = self.get_object()  # Получаем операцию
        serializer = self.get_serializer(
            operation_instance, data=request.data, partial=True
        )


        if serializer.is_valid(raise_exception=True):
            if operation_instance.type == "TARGETS":
                if operation_instance.categories:
                    raise ReturnMoneyCategoryOperationError()

                target_instance = Target.objects.get(id=operation_instance.target.pk)

                if request.data.get("amount"):
                    target_instance.current_sum -= (operation_instance.amount - Decimal(request.data['amount']))

                    if target_instance.current_sum > target_instance.amount:
                        raise ExceedingTargetAmountError()
                    elif target_instance.current_sum == target_instance.amount:
                        target_instance.status = "ACHIEVED"
                    else:
                        target_instance.status = "IN_PROGRESS"
                    target_instance.save()

                elif request.data.get("date"):
                    if datetime.strptime(request.data["date"], "%Y-%m-%d").replace(tzinfo=None) < target_instance.created_at.replace(tzinfo=None):
                        raise InvalidTargetOperationDateError()

            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)