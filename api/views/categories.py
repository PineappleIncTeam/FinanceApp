from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (DestroyAPIView, ListCreateAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from api.models import Category
from api.serializers import CategoriesSerializer, CategoryDetailSerializer
from api.utils import get_user_categories
from api.views.errors import CategoryWithOperationsError

if TYPE_CHECKING:
    from django.db.models import QuerySet


logger = logging.getLogger(__name__)


class CategoriesListCreateAPI(ListCreateAPIView):
    """
    To get a list of user's categories and create a new category.
    """

    serializer_class = CategoriesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_income', 'is_outcome', 'is_deleted']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Category]:
        return get_user_categories(
            user=self.request.user
        )


class CategoryUpdateDestroyAPI(UpdateAPIView, DestroyAPIView):
    """
    To delete a category if there are no operations related with this category.
    To archive a category.
    """

    serializer_class = CategoryDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Category]:
        return get_user_categories(
            user=self.request.user
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.operations.exists():
            logger.error(
                f"The user [ID: {request.user.pk}, "
                f"name: {request.user.email}] can not delete a category "
                f"with existing operations: id {instance.pk}."
            )

            raise CategoryWithOperationsError()

        self.perform_destroy(instance)

        logger.info(
            f"The user [ID: {request.user.pk}, "
            f"name: {request.user.email}] has deleted a category: "
            f"id {instance.id}, name - {instance.name}."
        )
        return Response(status=HTTP_204_NO_CONTENT)
