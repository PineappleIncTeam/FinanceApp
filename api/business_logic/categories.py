from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Type, Union

from api.models import IncomeCategories

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from api.models import OutcomeCategories, User


logger = logging.getLogger(__name__)


def get_categories(
    user: User, category_model: Union[Type[IncomeCategories], Type[OutcomeCategories]]
) -> QuerySet[Union[IncomeCategories, OutcomeCategories]]:
    """
    Retrieve all user's incomes/outcomes categories which is not hidden.
    """

    if category_model is IncomeCategories:
        query_result = (
            category_model.objects.prefetch_related("incomes_set")
            .filter(incomes__user=user.pk, incomes__is_hidden=False)
            .distinct("incomes__category")
        )
    else:
        query_result = (
            category_model.objects.prefetch_related("outcomes_set")
            .filter(outcomes__user=user.pk, outcomes__is_hidden=False)
            .distinct("outcomes__category")
        )

    logger.info(
        f"The user [ID: {user.pk}, "
        f"name: {user.email}] successfully received "
        f"a list of the users's {category_model} categories."
    )

    return query_result
