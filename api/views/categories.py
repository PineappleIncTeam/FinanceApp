from __future__ import annotations

import logging

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from unicodedata import category

from api.models import Category, Operation
from api.serializers import CategoriesSerializer, CategoryDetailSerializer
from api.serializers.category import CategoriesGetSerializer
from api.serializers.profile import ErrorSerializer
from api.utils import get_user_categories
from api.views.errors import CategoryWithOperationsError, SystemCategoryError


logger = logging.getLogger(__name__)


class CategoriesListCreateAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategoriesSerializer

    @swagger_auto_schema(
        operation_id='Создание новой категории',
        operation_description='Создание новой категории',
        responses={
            200: openapi.Response(description="Категория успешно создана", schema=CategoriesSerializer),
            401: openapi.Response(description="Неавторизованный запрос",
                                  schema=ErrorSerializer),
            403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
            409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации",
                                  schema=ErrorSerializer),
            500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
            503: openapi.Response(description="Сервер не готов обработать запрос в данный момент",
                                  schema=ErrorSerializer),
        })
    def post(self, request, *args, **kwargs):
        serializer = CategoriesSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryGetAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategoriesGetSerializer

    @swagger_auto_schema(
        operation_id='Получение списка категорий пользователя',
        operation_description='Фильтрация по типу категории (расход/доход)',
        manual_parameters=[
            openapi.Parameter(
                name="is_outcome",
                in_=openapi.IN_QUERY,
                description="Фильтр по расходам (True/False)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                name="is_income",
                in_=openapi.IN_QUERY,
                description="Фильтр по доходам (True/False)",
                type=openapi.TYPE_BOOLEAN
            )
        ],
        responses={
            200: openapi.Response(description="Список категорий успешно получен",
                                  schema=CategoriesGetSerializer(many=True)),
            401: openapi.Response(description="Неавторизованный запрос", schema=ErrorSerializer),
            403: openapi.Response(description="Доступ запрещен", schema=ErrorSerializer),
            409: openapi.Response(description="Ошибка при получении данных", schema=ErrorSerializer),
            500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
            503: openapi.Response(description="Сервер временно недоступен", schema=ErrorSerializer),
        }
    )
    def get(self, request, *args, **kwargs):
        """Фильтрация категорий по типу (доход/расход)"""
        queryset = Category.objects.filter(user=request.user, is_deleted=False)

        # Получаем query параметры
        is_outcome = request.GET.get("is_outcome")
        is_income = request.GET.get("is_income")

        # Конвертируем строковые параметры в булевые значения
        def str_to_bool(value):
            return str(value).lower() in ["true", "1", "yes"]

        if is_outcome is not None:
            queryset = queryset.filter(is_outcome=str_to_bool(is_outcome))

        if is_income is not None:
            queryset = queryset.filter(is_income=str_to_bool(is_income))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryUpdateDestroyAPI(GenericAPIView):
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_user_categories(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        category_id = self.kwargs.get('pk')
        try:
            category = queryset.get(id=category_id)
        except Category.DoesNotExist:
            raise NotFound("Категория не найдена")
        return category


    @swagger_auto_schema(
        operation_id='Архивирование категории',
        operation_description='Архивирование категории по уникальному идентификатору',
    responses = {
        200: openapi.Response(description="Категория успешно архивирована", schema=CategoryDetailSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        404: openapi.Response(description="Категория не найдена", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def put(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            logger.info(
                "The user [ID: %s, "
                "name: %s] has updated a category: "
                "id %s, name - %s.",
                request.user.pk,
                request.user.email,
                category.id,
                category.name
            )
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_id='Удаление категории',
        operation_description='Удаление категории по уникальному идентификатору, если с этой категорией не выполняются никакие операции',
    responses = {
        200: openapi.Response(description="Категория успешно удалена", schema=CategoryDetailSerializer),
        401: openapi.Response(description="Неавторизованный запрос",
                              schema=ErrorSerializer),
        403: openapi.Response(description="Доступ запрещен/не хватает прав", schema=ErrorSerializer),
        404: openapi.Response(description="Категория не найдена", schema=ErrorSerializer),
        409: openapi.Response(description="Произошла непредвиденная ошибка при получении информации", schema=ErrorSerializer),
        500: openapi.Response(description="Ошибка сервера", schema=ErrorSerializer),
        503: openapi.Response(description="Сервер не готов обработать запрос в данный момент", schema=ErrorSerializer),
    })
    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        if category.is_system is True:
            raise SystemCategoryError()
        if category.operations.exists():
            logger.error(
                "The user [ID: %s, "
                "name: %s] cannot delete a category "
                "with existing operations: id %s.",
                request.user.pk,
                request.user.email,
                category.pk
            )
            raise CategoryWithOperationsError()

        category.is_deleted = True
        category.save()

        logger.info(
            "The user [ID: %s, "
            "name: %s] has archived category: "
            "id %s, name - %s.",
            request.user.pk,
            request.user.email,
            category.id,
            category.name
        )
        return Response({"detail": "Категория успешна удалена"},status=status.HTTP_200_OK)
