from __future__ import annotations

import logging

from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import IN_PROGRESS
from api.serializers import TargetsSerializer
from api.utils import get_user_targets, return_money_from_target_to_incomes

from ..serializers.profile import ErrorSerializer
from rest_framework.generics import GenericAPIView

from api.models import Target


logger = logging.getLogger(__name__)


class TargetsListCreateAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TargetsSerializer


    @swagger_auto_schema(
        operation_id='Получение списка целей пользователя',
        operation_description='Получение списка целей пользователя',
    responses = {
        200: openapi.Response(description="Список целей успешно получен", schema=TargetsSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def get(self, request, *args, **kwargs):
        queryset = get_user_targets(user=request.user)

        is_deleted = request.query_params.get('is_deleted')
        if is_deleted is not None:
            queryset = queryset.filter(is_deleted=is_deleted)

        serializer = TargetsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_id='Создание новой цели',
        operation_description='создание новой цели',
    responses = {
        200: openapi.Response(description="Цель успешно создана", schema=TargetsSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def post(self, request, *args, **kwargs):
        serializer = TargetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TargetUpdateDestroyAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TargetsSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return get_user_targets(user=self.request.user)

    def get_object(self, pk):
        try:
            return get_user_targets(self.request.user).filter(pk=pk)
        except Target.DoesNotExist:
            raise NotFound(detail="Цель не найдена")


    @swagger_auto_schema(
        operation_id='Изменение цели',
        operation_description='Изменение цели по уникальному индентификатору',
    responses = {
        200: openapi.Response(description="Цель успешно изменена", schema=TargetsSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def put(self, request, *args, **kwargs):
        instance = self.get_object(kwargs['pk'])
        serializer = TargetsSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_id='Закрытие цели',
        operation_description='Закрытие цели по уникальному индентификатору',
    responses = {
        200: openapi.Response(description="Цель успешно закрыта", schema=TargetsSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        409: openapi.Response(description="Цель находится в процессе", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def delete(self, request, *args, **kwargs):
        instance = self.get_object(kwargs['pk'])

        if instance.is_deleted:
            return Response({"detail": "Цель уже закрыта."}, status=status.HTTP_404_NOT_FOUND)

        if instance.status == IN_PROGRESS:
            return Response({"detail": "Цель находится в процессе."}, status=status.HTTP_409_CONFLICT)

        try:
            returned_operation = return_money_from_target_to_incomes(user=request.user, target=instance)
            instance.is_deleted = True
            instance.current_sum = 0
            instance.save()

            logger.info(
                "The user [ID: %s] closed a target: "
                "id %s, name - %s, returned amount - %s.",
                request.user.pk,
                instance.id,
                instance.name,
                returned_operation.amount,
            )

            return Response(data=TargetsSerializer(instance).data, status=status.HTTP_200_OK)

        except IntegrityError:
            return Response({"detail": "Не удалось вернуть деньги с цели на доходы."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_id='Получить цель',
        operation_description='Получить цель по уникальному идентификатору',
        responses={
            200: openapi.Response(description="Цель успешно получена ", schema=TargetsSerializer),
            401: openapi.Response(description="Неавторизованный запрос",
                                  schema=ErrorSerializer),
            403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
            409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации",
                                  schema=ErrorSerializer),
            500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
            503: openapi.Response(description="Сервер не готов обработать запрос в данный момент",
                                  schema=ErrorSerializer),
        })
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        target = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = self.get_serializer(target)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TargetMoneyReturnAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return get_user_targets(user=self.request.user)

    @swagger_auto_schema(
        operation_id='Удаление цели',
        operation_description='Удаление цели по уникальному индентификатору',
    responses = {
        200: openapi.Response(description="Цель успешно удалена", schema=TargetsSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        404: openapi.Response(description="Нет цели с таким id", schema=ErrorSerializer),
        409: openapi.Response(description="Цель находится в процессе", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        target = get_object_or_404(queryset, pk=kwargs['pk'])
        target.delete()
        return Response({"detail": "Цель успешно удалена"}, status=status.HTTP_200_OK)
