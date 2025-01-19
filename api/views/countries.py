from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Country
from api.serializers import CountrySerializer
from api.serializers.profile import ErrorSerializer


class CountriesApiView(GenericAPIView):
    @swagger_auto_schema(
        operation_id='Получение списка стран',
        operation_description='Получение списка всех стран',
    responses = {
        200: openapi.Response(description="Все страны успешно получены", schema=CountrySerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def get(self, request, *args, **kwargs):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)