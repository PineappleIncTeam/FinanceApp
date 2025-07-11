from rest_framework import status
from rest_framework.generics import GenericAPIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import requests
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


class ChequeView(GenericAPIView):
    parser_classes = [MultiPartParser]
    
    @swagger_auto_schema(
        operation_id='Получение выписки в формате pdf',
        operation_description='Получение PDF файла с операциями и диаграммой',
        manual_parameters=[
            openapi.Parameter(
                name="photo",
                in_=openapi.IN_FORM,
                description="фото чека",
                type=openapi.TYPE_FILE,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(description="PDF файл успешно получен"),
            500: openapi.Response(description="Ошибка генерации отчёта")
        }
    )
    def post(self, request):
        cheque_file = request.FILES.get("photo")

        if not cheque_file:
            return Response({"error": "Файл 'photo' не передан"}, status=status.HTTP_400_BAD_REQUEST)
        url = 'https://proverkacheka.com/api/v1/check/get'

        data = {'token': '34462.juLaZk5Pfgsw4khiA'}

        files = {'qrfile': cheque_file}

        r = requests.post(url, data=data, files=files)

        r = r.json()
        items = r["data"]["json"]["items"]
        result = []
        for item in items:
            result.append(
                {
                    "name": item["name"],
                    "quantity": item["quantity"],
                    "price_per_unit": item["price"] / 100,
                    "total": item["sum"] / 100
                }
            )
        result.append({"sum": r["request"]["manual"]["sum"]})
        return Response(result, status=status.HTTP_200_OK)