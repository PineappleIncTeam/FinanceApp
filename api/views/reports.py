from django.db.models import Sum, Case, When, F, Value, Q, DecimalField
from django.db.models.functions import TruncMonth
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, date

from api.models import Operation
from api.models.operation import INCOME_CATEGORY, OUTCOME_CATEGORY
from api.serializers.reports import CategoryAggregationSerializer


class ReportView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BalanceSerializer

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({"error": "All parameters must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            if start_date_obj > end_date_obj:
                return Response(
                    {"error": "Start date must be before end date."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        operations = Operation.objects.filter(
            Q(user=request.user) &
            Q(date__gte=start_date_obj) &
            Q(date__lte=end_date_obj)
        ).aggregate(
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

        return Response({
            "total_expenses": operations['total_expenses'] or 0,
            "total_income": operations['total_income'] or 0,
            "total_savings": operations['total_savings'] or 0,
        })


class OperationAggregationView(GenericAPIView):
    def get(self, request):
        operation_type = request.query_params.get('type')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not operation_type or not start_date or not end_date:
            return Response({"error": "All parameters must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        if operation_type not in [INCOME_CATEGORY, OUTCOME_CATEGORY]:
            return Response({"error": "Invalid operation type."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            if start_date_obj > end_date_obj:
                return Response(
                    {"error": "Start date must be before end date."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        operations = Operation.objects.filter(
            type=operation_type,
            categories__isnull=False,
            date__range=[start_date, end_date]
        )

        aggregated_data = operations.annotate(
            month=TruncMonth('date')
        ).values('categories__id', 'categories__name', 'month').annotate(
            total=Sum('amount')
        ).order_by('month')

        results = {}

        for entry in aggregated_data:
            category_id = entry['categories__id']
            category_name = entry['categories__name']
            month = entry['month'].strftime('%Y-%m')
            amount = entry['total']

            if category_id not in results:
                results[category_id] = {
                    'category_id': category_id,
                    'category_name': category_name,
                    'month_sums': []
                }

            results[category_id]['month_sums'].append({
                'month': month,
                'amount': amount
            })

        return Response(CategoryAggregationSerializer(list(results.values()), many=True).data)
