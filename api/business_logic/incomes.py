from __future__ import annotations
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from api.models import Incomes
from .errors import InvalidNumberOfItemsError

from django.db.models import Sum


if TYPE_CHECKING:
    from django.db.models import QuerySet
    from api.models import User


logger = logging.getLogger(__name__)


def get_incomes(
        user: User,
        order_by: Optional[str] = None,
        number_of_items: Optional[int] = None
) -> QuerySet[Incomes]:
    """
    Retrieve all user's incomes.

    Args:
        order_by (str | None): Condition for ordering
        number_of_items (int | None): An amount of objects are to be retrieved.
    """

    if not order_by:
        user_incomes = Incomes.objects.filter(
            user=user.pk
        ).order_by("-created_at")
    else:
        user_incomes = Incomes.objects.filter(user=user.pk).order_by(order_by)

    try:
        if number_of_items:
            user_incomes = user_incomes[:number_of_items]
            logger.info(
                f"The user [ID: {user.pk}, "
                f"name: {user.email}] successfully received "
                f"a list of last {number_of_items} the users's Incomes."
            )
    except IndexError:
        logger.error(
            f"The user [ID: {user.pk}, "
            f"name: {user.email}] - invalid parameter 'number_of_items':"
            f" {number_of_items} - to receive the users's Incomes."
        )
        raise InvalidNumberOfItemsError

    return user_incomes.select_related('category').values(
        'id',
        'sum',
        'category__name',
        'created_at'
    )


def get_sum_of_incomes_in_current_month(user: User) -> float:
    """
    Retrieve total amount of user's incomes in the current month.
    If there is no income in the current month this function returns 0.00.
    """

    current_month = datetime.now().month
    result = (
        get_incomes(user=user)
        .filter(created_at__month=current_month)
        .aggregate(total_sum=Sum('sum'))
    ).get('total_sum')

    if not result:
        logger.info(
            f"The user [ID: {user.pk}, "
            f"name: {user.email}] - there is no incomes in the current month."
        )
        return float(0)

    logger.info(
        f"The user [ID: {user.pk}, "
        f"name: {user.email}] - successfully return a total amount "
        f"of incomes in current month."
    )

    return float(result)
