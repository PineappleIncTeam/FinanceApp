from __future__ import annotations

import logging
from datetime import date
from typing import TYPE_CHECKING, Optional

from django.db import transaction

from api.models import FROM_TARGETS, Category, Operation, Target

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from api.models import User


logger = logging.getLogger(__name__)


def get_user_categories(
    user: User,
    is_income: Optional[bool] = None,
    is_outcome: Optional[bool] = None,
    is_deleted: Optional[bool] = None
) -> QuerySet[Category]:
    """
    Retrieve user's categories.
    """

    query_result = Category.objects.filter(user=user.pk)

    if is_income is not None:
        query_result = query_result.filter(
            is_income=is_income
        )

    if is_outcome is not None:
        query_result = query_result.filter(
            is_outcome=is_outcome
        )

    if is_deleted is not None:
        query_result = query_result.filter(
            is_deleted=is_deleted
        )

    logger.info(
        f"The user [ID: {user.pk}, "
        f"name: {user.email}] successfully received "
        f"a list of the users's categories."
    )

    return query_result


def get_user_targets(
    user: User
) -> QuerySet[Target]:
    """
    Retrieve user's targets.
    """

    query_result = Target.objects.filter(
        user=user.pk
    )

    logger.info(
        f"The user [ID: {user.pk}, "
        f"name: {user.email}] successfully received "
        f"a list of the users's targets."
    )

    return query_result


def get_total_target_amount(
    target: Target
) -> int:
    """
    Return total amount of user's particular target.
    """
    result = Operation.objects.filter(target=target.pk).aggregate("amount")
    return result["amount"]


def return_money_from_target_to_incomes(
    user: User, target: Target
) -> Operation:
    with transaction.atomic():
        category = Category.objects.get_or_create(
            user=user,
            name="из накоплений",
            is_income=False,
            is_outcome=False
        )
        returned_operation = Operation.objects.create(
            user=user,
            type=FROM_TARGETS,
            categories=category[0],
            amount=target.current_sum,
            date=date.today()
        )
    return returned_operation
