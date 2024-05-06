from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from api.models import IncomeCategories

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from api.models import User


logger = logging.getLogger(__name__)


def get_income_categories(user: User) -> QuerySet[IncomeCategories]:
    """
    Retrieve all user's incomes categories which is not hidden.
    """

    query_result = (
        IncomeCategories.objects.prefetch_related("incomes_set")
        .filter(incomes__user=user.pk, incomes__is_hidden=False)
        .distinct("incomes__category")
    )

    logger.info(
        f"The user [ID: {user.pk}, "
        f"name: {user.email}] successfully received "
        f"a list of the users's Incomecategories."
    )

    return query_result
