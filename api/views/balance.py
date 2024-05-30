from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from api.business_logic import get_balance

if TYPE_CHECKING:
    from rest_framework.request import Request


class BalanceGetAPI(APIView):
    """
    Return a total user's balance in current date.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:

        current_date = request.data.get("date")
        total_sum = get_balance(
            user=request.user,
            date=current_date
        )

        return Response(data={"sum_balance": total_sum}, status=HTTP_200_OK)
