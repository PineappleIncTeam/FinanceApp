from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from api.models import IncomeCategories

if TYPE_CHECKING:
    from django.db.models import Model, QuerySet

    from api.models import User


logger = logging.getLogger(__name__)


def get_categories(user: User, category_instanse: Model) -> QuerySet[Model]:
    """
    Retrieve all user's incomes/outcomes categories which is not hidden.
    """
    if isinstance(category_instanse, IncomeCategories):
        query_result = (
            category_instanse.objects.prefetch_related("incomes_set")
            .filter(incomes__user=user.pk, incomes__is_hidden=False)
            .distinct("incomes__category")
        )
    else:
        query_result = (
            category_instanse.objects.prefetch_related("outcomes_set")
            .filter(outcomes__user=user.pk, outcomes__is_hidden=False)
            .distinct("outcomes__category")
        )

    logger.info(
        f"The user [ID: {user.pk}, "
        f"name: {user.email}] successfully received "
        f"a list of the users's {category_instanse} categories."
    )

    return query_result
