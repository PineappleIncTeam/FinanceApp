from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import JsonResponse
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.business_logic import get_finance, get_sum_of_finance_in_current_month
from api.models import Incomes
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

    def get_queryset(self) -> QuerySet[Incomes]:
        result = get_finance(user=self.request.user, finance_model=Incomes)
        return result


class IncomeSumInCurrentMonthGetAPI(APIView):
    """
    Return a total sum of user's incomes in current mounth.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        total_sum = get_sum_of_finance_in_current_month(
            user=request.user, finance_model=Incomes
        )
        return JsonResponse({"sum_balance": total_sum})


class LastIncomesGetAPI(ListAPIView):
    """
    To get a list of last user's incomes.
    """

    serializer_class = IncomeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Incomes]:
        """
        To get last user's incomes.
        The amount of income displayed is passed by the items parameter
        in the query parameters.
        """

        items = int(self.request.GET.get("items"))
        result = get_finance(
            user=self.request.user,
            finance_model=Incomes,
            number_of_items=items
        )
        return result


class IncomeCreateAPI(CreateAPIView):
    serializer_class = IncomeCreateSerializer
    permission_classes = (IsAuthenticated,)
