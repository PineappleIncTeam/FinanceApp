from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.business_logic import get_categories
from api.models import OutcomeCategories
from api.serializers import OutcomeCategoriesSerializer

if TYPE_CHECKING:
    from django.db.models import QuerySet


class OutcomeCategoriesListCreateAPI(ListCreateAPIView):
    """
    To get a list of user's outcome categories and create a new outcome category.
    """

    serializer_class = OutcomeCategoriesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[OutcomeCategories]:
        return get_categories(
            user=self.request.user, category_model=OutcomeCategories
        )
