from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from api.business_logic import get_sum_of_finance_in_current_month, get_finance
from api.models import Outcomes
from api.serializers import OutcomeSerializer, OutcomeRetrieveSerializer

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.request import Request
    from rest_framework.response import Response


class OutcomeSumInCurrentMonthGetAPI(APIView):
    """
    Return a total sum of user's outcomes in current mounth.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        user = request.user
        total_sum = get_sum_of_finance_in_current_month(
            user=user, finance_model=Outcomes
        )
        return JsonResponse({"sum_balance": total_sum})


class LastOutcomesGetAPI(ListAPIView):
    """
    To get a list of last user's outcomes.
    """

    serializer_class = OutcomeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Outcomes]:
        """
        To get last user's outcomes.
        The amount of outcome displayed is passed by the <items> parameter
        in the query parameters.
        """

        items = int(self.request.GET.get("items"))
        result = get_finance(
            user=self.request.user, finance_model=Outcomes, number_of_items=items
        )
        return result


class OutcomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    """Retrieve, update outcomes"""

    queryset = Outcomes.objects.all()
    serializer_class = OutcomeRetrieveSerializer
    permission_classes = (IsAuthenticated,)