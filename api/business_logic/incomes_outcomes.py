from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union

from django.db.models import Sum

from .errors import InvalidNumberOfItemsError

if TYPE_CHECKING:
    from django.db.models import Model, QuerySet

    from api.models import Incomes, Outcomes, User


logger = logging.getLogger(__name__)


def get_finance(
    user: User,
    instance: Model,
    order_by: Optional[str] = None,
    number_of_items: Optional[int] = None,
) -> QuerySet[Union[Incomes, Outcomes]]:
    """
    Retrieve all user's incomes or uotcomes.

    Args:
        order_by (str | None): Condition for ordering
        number_of_items (int | None): An amount of objects are to be retrieved.
    """

    if not order_by:
        finances = instance.objects.filter(user=user.pk).order_by("-created_at")
    else:
        finances = instance.objects.filter(user=user.pk).order_by(order_by)

    try:
        if number_of_items:
            finances = finances[:number_of_items]
            logger.info(
                f"The user [ID: {user.pk}, "
                f"name: {user.email}] successfully received "
                f"a list of last {number_of_items} the users's {instance}."
            )
    except IndexError:
        logger.error(
            f"The user [ID: {user.pk}, "
            f"name: {user.email}] - invalid parameter 'number_of_items':"
            f" {number_of_items} - to receive the users's {instance}."
        )
        raise InvalidNumberOfItemsError

    return finances.select_related("category").values(
        "id", "sum", "category__name", "created_at"
    )


def get_sum_of_finance_in_current_month(user: User, instance: Model) -> float:
    """
    Retrieve total amount of user's incomes or utcomes in the current month.
    If there is no incomes/outcomes in the current month this function returns 0.00.
    """

    current_month = datetime.now().month
    result = (
        get_finance(user=user, instance=instance)
        .filter(created_at__month=current_month)
        .aggregate(total_sum=Sum("sum"))
    ).get("total_sum")

    if not result:
        logger.info(
            f"The user [ID: {user.pk}, "
            f"name: {user.email}] - there is no {instance} in the current month."
        )
        return float(0)

    logger.info(
        f"The user [ID: {user.pk}, "
        f"name: {user.email}] - successfully return a total amount "
        f"of {instance} in current month."
    )

    return float(result)
