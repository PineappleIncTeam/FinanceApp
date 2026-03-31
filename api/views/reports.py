from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.db.models import Sum, Q, Coalesce, Value  # добавлено Coalesce, Value

from api.models import Operation, Category, Target
from api.serializers.profile import ErrorSerializer
from api.serializers.reports import (BalanceSerializer,
                                     ReportCategorySerializer,
                                     StatisticsSerializer)
from api.utils import (get_and_check_date_params, get_category_report_data,
                       get_summary_data)


# ... остальные классы ReportBalanceView, ReportStatisticsView без изменений ...

class ReportCategoriesView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReportCategorySerializer

    @swagger_auto_schema(
        # ... документация без изменений ...
    )
    def get(self, request: Request) -> Response:
        operation_type = request.query_params.get("type")
        start_date, end_date = get_and_check_date_params(
            request.query_params.get("start_date"),
            request.query_params.get("end_date"),
        )

        if operation_type:
            if operation_type == "target":
                operation_type = "targets"

            try:
                results = get_category_report_data(request.user, operation_type, start_date, end_date)
            except TypeError:
                results = self._get_category_report_data_directly(
                    request.user, operation_type, start_date, end_date
                )

            formatted_results = []
            for item in results:
                if 'total' in item:
                    item_data = {
                        'category_id': item.get('category_id'),
                        'category_name': item.get('category_name'),
                        'amount': item['total'],
                        'items': item.get('items', [])
                    }
                else:
                    item_data = {
                        'category_id': item.get('category_id'),
                        'category_name': item.get('category_name'),
                        'amount': item.get('amount'),
                        'items': item.get('items', [])
                    }
                formatted_results.append(item_data)

            serialized = ReportCategorySerializer(formatted_results, many=True).data

            return Response({
                "is_income": operation_type == "income",
                "is_outcome": operation_type == "outcome",
                "is_target": operation_type == "targets",
                "results": serialized,
            })

        else:
            incomes = self._get_category_report_data_directly(
                request.user, "income", start_date, end_date
            )
            outcomes = self._get_category_report_data_directly(
                request.user, "outcome", start_date, end_date
            )
            targets = self._get_category_report_data_directly(
                request.user, "targets", start_date, end_date
            )

            def format_data(data, add_items=False):
                formatted = []
                for item in data:
                    if 'total' in item:
                        item_data = {
                            'category_id': item.get('category_id'),
                            'category_name': item.get('category_name'),
                            'amount': item['total'],
                            'items': item.get('items', [])
                        }
                    else:
                        item_data = {
                            'category_id': item.get('category_id'),
                            'category_name': item.get('category_name'),
                            'amount': item.get('amount'),
                            'items': item.get('items', [])
                        }
                    if add_items:
                        item_data['items'] = self._get_operation_details(
                            request.user, item_data['category_id'], start_date, end_date
                        )
                    formatted.append(item_data)
                return formatted

            formatted_incomes = format_data(incomes)
            formatted_outcomes = format_data(outcomes)
            formatted_targets = format_data(targets)

            def calculate_total(data):
                return sum(item['amount'] for item in data) if data else 0

            total_incomes = calculate_total(formatted_incomes)
            total_outcomes = calculate_total(formatted_outcomes)
            total_targets = calculate_total(formatted_targets)
            balance = total_incomes - total_outcomes - total_targets

            incomes_serialized = ReportCategorySerializer(formatted_incomes, many=True).data
            outcomes_serialized = ReportCategorySerializer(formatted_outcomes, many=True).data
            targets_serialized = ReportCategorySerializer(formatted_targets, many=True).data

            return Response({
                "incomes": incomes_serialized,
                "outcomes": outcomes_serialized,
                "targets": targets_serialized,
                "summary": {
                    "total_incomes": total_incomes,
                    "total_outcomes": total_outcomes,
                    "total_targets": total_targets,
                    "balance": balance,
                }
            })

    def _get_category_report_data_directly(self, user, operation_type, start_date, end_date):
        """
        Получение данных по категориям/целям, включая операции без категории/цели.
        Операции без категории/цели группируются под именем "Без категории"/"Без цели".
        """
        from django.db.models import Sum, Coalesce, Value  # уже импортировано вверху, но для надёжности оставим

        queryset = Operation.objects.filter(user=user)

        if operation_type:
            queryset = queryset.filter(type=operation_type)

        if start_date and end_date:
            queryset = queryset.filter(date__range=(start_date, end_date))

        if operation_type == "targets":
            # Для накоплений группируем по цели, включая операции без цели
            results = queryset.annotate(
                target_id=Coalesce('target__id', Value(-1)),
                target_name=Coalesce('target__name', Value('Без цели'))
            ).values('target_id', 'target_name').annotate(
                total=Sum('amount')
            ).order_by('-total')

            formatted_results = []
            for item in results:
                category_id = item['target_id'] if item['target_id'] != -1 else None
                formatted_results.append({
                    'category_id': category_id,
                    'category_name': item['target_name'],
                    'total': item['total']
                })
            return formatted_results
        else:
            # Для доходов/расходов группируем по категории, включая операции без категории
            results = queryset.annotate(
                category_id=Coalesce('categories__id', Value(-1)),
                category_name=Coalesce('categories__name', Value('Без категории'))
            ).values('category_id', 'category_name').annotate(
                total=Sum('amount')
            ).order_by('-total')

            formatted_results = []
            for item in results:
                category_id = item['category_id'] if item['category_id'] != -1 else None
                formatted_results.append({
                    'category_id': category_id,
                    'category_name': item['category_name'],
                    'total': item['total']
                })
            return formatted_results

    def _get_operation_details(self, user, category_id, start_date, end_date):
        """Получение детализации операций для категории (может быть None для группы "Без категории")."""
        queryset = Operation.objects.filter(user=user)

        if category_id is not None:
            queryset = queryset.filter(categories_id=category_id)
        else:
            # Для операций без категории
            queryset = queryset.filter(categories__isnull=True)

        if start_date and end_date:
            queryset = queryset.filter(date__range=(start_date, end_date))

        # Возвращаем список операций с основными полями
        return list(queryset.values('id', 'amount', 'date', 'type'))