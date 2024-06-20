from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional, Type, Union

from api.models import IncomeCategories, Targets

from .errors import TargetDoesNotExistError

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

    elif category_model is Targets:
        query_result = (
            category_model.objects
            .filter(user=user.pk, is_hidden=False)
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


def archive_accumulation_target(user: User, target_id: Optional[Any]) -> Targets:
    """
    To set 'is_hidden' field in the Targets instance to True.
    """
    try:
        target = Targets.objects.get(pk=target_id)
    except Targets.DoesNotExist:
        logger.error(
            f"The user [ID: {user.pk}, "
            f"name: {user.email}] requested to archive a target {target_id}. "
            f"Such target {target_id} doesn't exist."
        )
        raise TargetDoesNotExistError(
            f"Such target {target_id} doesn't exist."
        )
    target.is_hidden = True
    target.save()

    logger.info(
        f"The user [ID: {user.pk}, "
        f"name: {user.email}] successfully archived "
        f"the Targets instance: {target_id}, {target.target_name}."
    )

    return target
