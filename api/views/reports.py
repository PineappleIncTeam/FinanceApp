from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from api.serializers.reports import (BalanceSerializer,
                                     ReportCategorySerializer,
                                     StatisticsSerializer)
from api.utils import (get_and_check_date_params, get_category_report_data,
                       get_summary_data)


class ReportBalanceView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BalanceSerializer

    def get(self, request: Request) -> Response:
        data = get_summary_data(request.user)

        return Response(
            data={"current_balance": data["total_income"] - data["total_expenses"] - data["total_savings"]},
            status=HTTP_200_OK,
        )


class ReportStatisticsView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StatisticsSerializer

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


class ReportCategoriesView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReportCategorySerializer

    def get(self, request):
        operation_type = request.query_params.get("type", "outcome")

        start_date, end_date = get_and_check_date_params(
            request.query_params.get("start_date"),
            request.query_params.get("end_date")
        )

        results = get_category_report_data(operation_type, end_date, start_date)

        return Response(ReportCategorySerializer(list(results.values()), many=True).data)
