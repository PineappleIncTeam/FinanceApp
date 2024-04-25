from __future__ import annotations
import logging
from typing import TYPE_CHECKING

from api.business_logic import get_income_categories

from api.serializers import IncomeCategoriesSerializer

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

if TYPE_CHECKING:
    from django.db.models import QuerySet


logger = logging.getLogger(__name__)


class IncomeCategoriesListCreateAPI(ListCreateAPIView):
    """
    To get a list of user's income categories and create a new income category.
    """

    serializer_class = IncomeCategoriesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        logger.info(
            f"The user [ID: {self.request.user.pk}, "
            f"name: {self.request.user}] requested "
            f"a list of the users's Incomecategories."
        )
        
        user = self.request.user
        query_result = get_income_categories(user=user)

        logger.info(
            f"The user [ID: {self.request.user.pk}, "
            f"name: {self.request.user}] successfully received "
            f"a list of the users's Incomecategories."
        )
        
        return query_result
