from django.db.models import Sum, Case, When, F, Value, Q, DecimalField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, date

from api.models import Operation
from api.models.operation import INCOME_CATEGORY, OUTCOME_CATEGORY
from api.serializers.reports import BudgetQueryParamsSerializer


class BudgetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = BudgetQueryParamsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        calc_date = serializer.validated_data.get('date', date.today())

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

        total_expenses = operations['total_expenses']
        total_income = operations['total_income']
        total_savings = operations['total_savings']
        total_budget = total_income - total_expenses - total_savings

        return Response(
            {
            'total_budget': total_budget,
            'total_expenses': total_expenses,
            'total_income': total_income,
            'total_savings': total_savings
            }
        )


class BudgetByCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({"error": "Both 'start_date' and 'end_date' are required."}, status=400)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        filters = Q(user=request.user) & Q(date__gte=start_date) & Q(date__lte=end_date)

        operations_by_category = Operation.objects.filter(filters).values('categories__name').annotate(
            total_amount=Sum(
                Case(
                    When(type='income', then=F('amount')),
                    When(type='outcome', then=-F('amount')),
                    output_field=DecimalField()
                )
            )
        ).order_by('categories__name')

        result = {}

        for operation in operations_by_category:
            category_name = operation['categories__name'] or 'Без категории'
            result[category_name] = operation['total_amount']

        return Response(result)