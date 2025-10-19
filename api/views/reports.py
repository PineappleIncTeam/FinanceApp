from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

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
    responses = {
        200: openapi.Response(description="Баланс успешно получен", schema=BalanceSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def get(self, request: Request) -> Response:
        data = get_summary_data(request.user)
        return Response(
            data={"current_balance": int(data["total_income"]) - int(data["total_expenses"]) - int(data["total_savings"])},
            status=HTTP_200_OK,
        )


class ReportStatisticsView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StatisticsSerializer


    @swagger_auto_schema(
        operation_id='Получение статистики по категориям',
        operation_description='Получение статистики по категориям',
    responses = {
        200: openapi.Response(description="Статистика успешно получена", schema=StatisticsSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
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
    responses = {
        200: openapi.Response(description="информация о расходах, доходах и накоплениях пользователя испешно получена", schema=ReportCategorySerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def get(self, request):
        operation_type = request.query_params.get("type", "outcome")

        start_date, end_date = get_and_check_date_params(
            request.query_params.get("start_date"),
            request.query_params.get("end_date")
        )

        results = get_category_report_data(operation_type, end_date, start_date)

        return Response(ReportCategorySerializer(list(results.values()), many=True).data)
