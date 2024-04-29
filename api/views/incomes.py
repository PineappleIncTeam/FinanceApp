from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.business_logic import get_incomes, get_sum_of_incomes_in_current_month
from api.serializers import IncomeCreateSerializer, IncomeSerializer

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.request import Request


class IncomesRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    """
    Provide the ability to retrieve, update or delete a model instance.
    """

    serializer_class = IncomeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"

    def get_queryset(self) -> QuerySet:
        result = get_incomes(user=self.request.user)
        return result


class IncomeSumInCurrentMonthGetAPI(APIView):
    """
    Return a total sum of user's incomes in current mounth.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        user = request.user
        total_sum = get_sum_of_incomes_in_current_month(user=user)

        return JsonResponse({"sum_balance": total_sum})


class IncomeCreateAPI(CreateAPIView):
    serializer_class = IncomeCreateSerializer
    permission_classes = (IsAuthenticated,)
