from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework import filters
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from api.models import Operation
from api.serializers import OperationSerializer

if TYPE_CHECKING:
    from django.db.models import QuerySet


class OperationListCreateAPI(ListCreateAPIView):
    """
    View for retrieving a list of operations for the current user and creating new operations.
    """

    serializer_class = OperationSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.BaseFilterBackend,)
    filter_fields = ["type"]

    def get_queryset(self) -> QuerySet[Operation]:
        return Operation.objects.filter(user=self.request.user)

    def filter_queryset(self, queryset):
        operation_type = self.request.query_params.get("type", None)
        if operation_type:
            queryset = queryset.filter(type=operation_type)

        last_five = self.request.query_params.get("last_five", None)
        if last_five and last_five.lower() == "true":
            queryset = queryset.order_by("-created_at")[:5]
        else:
            queryset = queryset.order_by("-created_at")

        return queryset


class OperationRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting an operation by its unique identifier (`pk`).
    """

    serializer_class = OperationSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"

    def get_queryset(self) -> QuerySet[Operation]:
        return Operation.objects.filter(user=self.request.user)
