from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.db.models import Sum, Q

from api.models import Operation, Category, Target
from api.serializers.profile import ErrorSerializer
from api.serializers.reports import (BalanceSerializer,
                                     ReportCategorySerializer,
                                     StatisticsSerializer)
from api.utils import (get_and_check_date_params, get_category_report_data,
                       get_summary_data)


class ReportBalanceView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BalanceSerializer

    @swagger_auto_schema(
        operation_id='Получение баланса',
        operation_description='Получение баланса пользователя',
        responses={
            200: openapi.Response(description="Баланс успешно получен", schema=BalanceSerializer),
            401: openapi.Response(description="Неавторизованный запрос",
                                  schema=ErrorSerializer),
            403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
            409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации",
                                  schema=ErrorSerializer),
            500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
            503: openapi.Response(description="Сервер не готов обработать запрос в данный момент",
                                  schema=ErrorSerializer),
        })
    def get(self, request: Request) -> Response:
        data = get_summary_data(request.user)
        return Response(
            data={"current_balance": int(data["total_income"]) - int(data["total_expenses"]) - int(
                data["total_savings"])},
            status=HTTP_200_OK,
        )


class ReportStatisticsView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StatisticsSerializer

    @swagger_auto_schema(
        operation_id='Получение статистики по категориям',
        operation_description='Получение статистики по категориям',
        responses={
            200: openapi.Response(description="Статистика успешно получена", schema=StatisticsSerializer),
            401: openapi.Response(description="Неавторизованный запрос",
                                  schema=ErrorSerializer),
            403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
            409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации",
                                  schema=ErrorSerializer),
            500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
            503: openapi.Response(description="Сервер не готов обработать запрос в данный момент",
                                  schema=ErrorSerializer),
        })
    def get(self, request):
        start_date, end_date = get_and_check_date_params(
            request.query_params.get("start_date"),
            request.query_params.get("end_date")
        )

        data = get_summary_data(request.user, start_date=start_date, end_date=end_date)

        return Response({
            "total_expenses": data["total_expenses"] or 0,
            "total_income": data["total_income"] or 0,
            "total_savings": data["total_savings"] or 0,
        })


class ReportCategoriesView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReportCategorySerializer

    @swagger_auto_schema(
        operation_id='Расходы/доходы/накопления пользователя',
        operation_description='Получение расходов, доходов и накоплений пользователя',
        responses={
            200: openapi.Response(
                description="Информация о расходах, доходах и накоплениях пользователя успешно получена",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "incomes": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_OBJECT),
                            description="Список доходов по категориям"
                        ),
                        "outcomes": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_OBJECT),
                            description="Список расходов по категориям"
                        ),
                        "targets": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_OBJECT),
                            description="Список накоплений по целям"
                        ),
                        "summary": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Сводная информация по всем операциям",
                            properties={
                                "total_incomes": openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                description="Общая сумма доходов"),
                                "total_outcomes": openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                 description="Общая сумма расходов"),
                                "total_targets": openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                description="Общая сумма накоплений"),
                                "balance": openapi.Schema(type=openapi.TYPE_NUMBER,
                                                          description="Баланс (доходы - расходы - накопления)"),
                            }
                        ),
                    },
                ),
            ),
            401: openapi.Response(description="Неавторизованный запрос", schema=ErrorSerializer),
            403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
            409: openapi.Response(description="Непредвиденная ошибка при получении информации", schema=ErrorSerializer),
            500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
            503: openapi.Response(description="Сервер не готов обработать запрос в данный момент",
                                  schema=ErrorSerializer),
        },
    )
    def get(self, request: Request) -> Response:
        operation_type = request.query_params.get("type")  # Убрали значение по умолчанию

        start_date, end_date = get_and_check_date_params(
            request.query_params.get("start_date"),
            request.query_params.get("end_date"),
        )

        # Если указан тип, возвращаем только его (для обратной совместимости)
        if operation_type:
            # Приводим тип к формату модели
            if operation_type == "target":
                operation_type = "targets"

            try:
                results = get_category_report_data(request.user, operation_type, start_date, end_date)
            except TypeError:
                results = self._get_category_report_data_directly(
                    request.user, operation_type, start_date, end_date
                )

            # Преобразуем данные в формат, ожидаемый сериализатором
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

        # Если тип не указан, возвращаем полный отчет по всем типам
        else:
            # Получаем данные по всем типам операций
            incomes = self._get_category_report_data_directly(
                request.user, "income", start_date, end_date
            )
            outcomes = self._get_category_report_data_directly(
                request.user, "outcome", start_date, end_date
            )
            targets = self._get_category_report_data_directly(
                request.user, "targets", start_date, end_date
            )

            # Преобразуем данные
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
                        # Можно добавить детализацию операций
                        item_data['items'] = self._get_operation_details(
                            request.user, item_data['category_id'], start_date, end_date
                        )
                    formatted.append(item_data)
                return formatted

            formatted_incomes = format_data(incomes)
            formatted_outcomes = format_data(outcomes)
            formatted_targets = format_data(targets)

            # Рассчитываем итоговые суммы
            def calculate_total(data):
                return sum(item['amount'] for item in data) if data else 0

            total_incomes = calculate_total(formatted_incomes)
            total_outcomes = calculate_total(formatted_outcomes)
            total_targets = calculate_total(formatted_targets)
            balance = total_incomes - total_outcomes - total_targets

            # Сериализуем
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
        """Альтернативная функция для получения данных по категориям"""

        # Базовый запрос фильтруем по пользователю
        queryset = Operation.objects.filter(user=user)

        # Фильтруем по типу операции
        if operation_type:
            queryset = queryset.filter(type=operation_type)

        # Фильтруем по датам
        if start_date and end_date:
            queryset = queryset.filter(date__range=(start_date, end_date))

        if operation_type == "targets":
            # Для накоплений группируем по целям
            results = queryset.filter(target__isnull=False).values(
                'target__id',
                'target__name'
            ).annotate(
                total=Sum('amount')
            ).order_by('-total')

            # Преобразуем в формат для сериализатора
            formatted_results = []
            for item in results:
                formatted_results.append({
                    'category_id': item['target__id'],
                    'category_name': item['target__name'],
                    'total': item['total']
                })
            return formatted_results
        else:
            # Для доходов/расходов группируем по категориям
            results = queryset.filter(categories__isnull=False).values(
                'categories__id',
                'categories__name'
            ).annotate(
                total=Sum('amount')
            ).order_by('-total')

            # Преобразуем в формат для сериализатора
            formatted_results = []
            for item in results:
                formatted_results.append({
                    'category_id': item['categories__id'],
                    'category_name': item['categories__name'],
                    'total': item['total']
                })
            return formatted_results

    def _get_operation_details(self, user, category_id, start_date, end_date):
        """Получение детализации операций для категории"""
        queryset = Operation.objects.filter(user=user, categories_id=category_id)

        if start_date and end_date:
            queryset = queryset.filter(date__range=(start_date, end_date))

        # Возвращаем список операций с основными полями
        return list(queryset.values('id', 'amount', 'date', 'type'))