import base64

from django.shortcuts import get_object_or_404
from drf_yasg.openapi import Schema, TYPE_OBJECT
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.models import Profile
from api.serializers import ProfileSerializer
from api.serializers.profile import ErrorSerializer


class ProfileApiView(RetrieveUpdateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    http_method_names = ['get', 'patch', 'head', 'options']

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    @swagger_auto_schema(
        operation_id='Получение профиля пользователя',
        operation_description='получение профиля пользователя',
    responses = {
        200: openapi.Response(description="Профиль успешно получен", schema=ProfileSerializer),
        401: openapi.Response(description="Неавторизованный запрос", schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_id='Изменение профиля пользователя',
        operation_description='Изменение данных профиля пользователя',
    responses = {
        200: openapi.Response(description="Профиль успешно изменен", schema=ProfileSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def patch(self, request, *args, **kwargs):
        import base64
        from rest_framework.response import Response
        from rest_framework import status

        partial = kwargs.pop('partial', True)
        profile = self.get_object()

        data = {
            'nickname': request.data.get('nickname'),
            'gender': request.data.get('gender'),
            'country': request.data.get('country'),
            'default': request.data.get('default')
        }

        uploaded_file = request.data.get('avatar')
        if uploaded_file:
            file_bytes = uploaded_file.read()
            base64_bytes = base64.b64encode(file_bytes)
            data['avatar'] = base64_bytes.decode('utf-8')

        serializer = self.get_serializer(profile, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"error_code": 400, "error_message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
