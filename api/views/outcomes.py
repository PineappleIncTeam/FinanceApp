from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.business_logic import get_sum_of_finance_in_current_month
from api.models import Outcomes

if TYPE_CHECKING:
    from rest_framework.request import Request
    from rest_framework.response import Response


class OutcomeSumInCurrentMonthGetAPI(APIView):
    """
    Return a total sum of user's outcomes in current mounth.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        user = request.user
        total_sum = get_sum_of_finance_in_current_month(user=user, instance=Outcomes)
        return JsonResponse({"sum_balance": total_sum})
