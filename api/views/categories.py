from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.business_logic import get_user_categories
from api.models import Category
from api.serializers import CategoriesSerializer

if TYPE_CHECKING:
    from django.db.models import QuerySet


class CategoriesListCreateAPI(ListCreateAPIView):
    """
    To get a list of user's income categories and create a new income category.
    """

    serializer_class = CategoriesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Category]:
        category_type = self.request.query_params.get('category_type')

        return get_user_categories(
            user=self.request.user,
            category_type=category_type,
            is_deleted=False
        )
