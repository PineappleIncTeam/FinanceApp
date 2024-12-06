from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from django.db.models import QuerySet
from rest_framework import filters, status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import ACHIEVED, IN_PROGRESS, TARGETS, Operation, Target
from api.serializers import OperationInfoSerializer, OperationSerializer
from FinanceBackend.settings import MAX_OPERATIONS_COUNT

from .errors import (ExceedingTargetAmountError,
                     InvalidTargetOperationDateError,
                     ReturnMoneyCategoryOperationError, TargetArchievedError,
                     TargetIsClosedError)


class OperationListCreateAPI(ListCreateAPIView):
    """
    получение списка операций для текущего пользователя
    """
    serializer_class = OperationSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.BaseFilterBackend,)
    filter_fields = ["type"]

    def get_queryset(self) -> QuerySet[Operation]:
        return Operation.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        создание новой операции
        """
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

    def filter_queryset(self, queryset):
        operation_type = self.request.query_params.get("type", None)
        if operation_type:
            if operation_type == TARGETS:
                queryset = queryset.filter(type=operation_type, categories=None)
            else:
                queryset = queryset.filter(type=operation_type)

        last_five = self.request.query_params.get("last_five", "true")
        if last_five and last_five.lower() == "true":
            queryset = queryset.order_by("-date", "-id")[:MAX_OPERATIONS_COUNT]
        else:
            queryset = queryset.order_by("-date", "-id")

        return queryset


class OperationRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = OperationInfoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"

    def get_queryset(self) -> QuerySet[Operation]:
        """
        получение операции по ее уникальному идентификатору
        """
        return Operation.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        """
        удаление операции по ее уникальному идентификатору
        """
        operation_instance: Operation = self.get_object()
        if operation_instance.type == TARGETS:
            if operation_instance.categories:
                raise ReturnMoneyCategoryOperationError()

            target_instance = Target.objects.get(
                id=operation_instance.target.pk
            )
            target_instance.current_sum -= operation_instance.amount
            target_instance.status = IN_PROGRESS
            target_instance.save()
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        обновление операции по ее уникальному идентификатору
        """
        operation_instance: Operation = self.get_object()
        serializer = self.get_serializer(
            operation_instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            if operation_instance.type == TARGETS:
                if operation_instance.categories:
                    raise ReturnMoneyCategoryOperationError()

                target_instance = Target.objects.get(
                    id=operation_instance.target.pk
                )
                if request.data.get("amount"):
                    target_instance.current_sum -= (
                        operation_instance.amount - request.data['amount'])

                    if target_instance.current_sum > target_instance.amount:
                        raise ExceedingTargetAmountError()
                    elif target_instance.current_sum == target_instance.amount:
                        target_instance.status = ACHIEVED
                    else:
                        target_instance.status = IN_PROGRESS
                    target_instance.save()

                elif request.data.get("date"):
                    if datetime.strptime(
                        request.data["date"], "%Y-%m-%d"
                    ).replace(tzinfo=None) < target_instance.created_at.replace(tzinfo=None):
                        raise InvalidTargetOperationDateError()

        return self.partial_update(request, *args, **kwargs)
