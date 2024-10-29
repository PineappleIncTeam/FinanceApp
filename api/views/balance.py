from __future__ import annotations

from datetime import date
import logging
from django.db.models import Sum, Case, When, F, Value, Q, DecimalField

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from api.models.operation import INCOME_CATEGORY, OUTCOME_CATEGORY, Operation
from rest_framework.views import APIView

from api.serializers.balance import BalanceSerializer


logger = logging.getLogger(__name__)

class BalanceGetAPI(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BalanceSerializer

    def get(self, request: Request) -> Response:
        calc_date = request.query_params.get('date', date.today())
        operations = Operation.objects.filter(Q(user=request.user) & Q(date__lte=calc_date)).aggregate(
            total_expenses=Sum(
                Case(
                    When(categories__isnull=False, type=OUTCOME_CATEGORY, then=F('amount')),
                    default=Value(0),
                    output_field=DecimalField()
                )
            ),
            total_income=Sum(
                Case(
                    When(categories__isnull=False, type=INCOME_CATEGORY, then=F('amount')),
                    default=Value(0),
                    output_field=DecimalField()
                )
            ),
            total_savings=Sum(
                Case(
                    When(target__isnull=False, then=F('amount')),
                    default=Value(0),
                    output_field=DecimalField()
                )
            ),
        )
        current_balance = operations['total_income'] - operations['total_expenses'] - operations['total_savings']

        logger.info(
            "The user [ID: %s, name: %s] - successfully returned a balance on the current date %s.",
            request.user.pk, request.user.email, calc_date
        )

        return Response(
            data={
                "current_balance": current_balance
            },
            status=HTTP_200_OK,
        )
