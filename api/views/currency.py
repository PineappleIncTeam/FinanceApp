from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.currency import CurrencyData
from api.serializers import CurrencyDataSerializer


class CurrencyDataView(APIView):
    @swagger_auto_schema(
        operation_id="Получение данных о валютах",
        operation_description="Получить данные о валютах из кэша или базы данных",
        responses={
            200: openapi.Response(
                description="Данные о валютах успешно получены", schema=CurrencyDataSerializer(many=True)
            ),
            503: openapi.Response(
                description="Данные недоступны",
                schema=openapi.Schema(type=openapi.TYPE_OBJECT, example={"error": "Data not available"}),
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        cached_data = cache.get("currency_data")

        if cached_data:
            return Response(cached_data)

        currencies = CurrencyData.objects.all()
        if not currencies:
            return Response({"error": "Data not available"}, status=503)

        serializer = CurrencyDataSerializer(currencies, many=True)

        cache.set("currency_data", serializer.data, timeout=4200)

        return Response(serializer.data)
