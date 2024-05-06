from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.business_logic import get_income_categories
from api.serializers import IncomeCategoriesSerializer

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from api.models import IncomeCategories


class IncomeCategoriesListCreateAPI(ListCreateAPIView):
    """
    To get a list of user's income categories and create a new income category.
    """

    serializer_class = IncomeCategoriesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[IncomeCategories]:
        return get_income_categories(user=self.request.user)
