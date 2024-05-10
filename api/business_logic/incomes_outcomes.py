from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union, Type

from django.db.models import Sum

from .errors import InvalidNumberOfItemsError

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from api.models import Incomes, Outcomes, User


logger = logging.getLogger(__name__)


def get_finance(
    user: User,
    finance_model: Union[Type[Incomes], Type[Outcomes]],
    order_by: Optional[str] = None,
    number_of_items: Optional[int] = None,
) -> QuerySet[Union[Incomes, Outcomes]]:
    """
    Retrieve all user's incomes or uotcomes.

    Args:
        order_by (str | None): Condition for ordering
        number_of_items (int | None): An amount of objects are to be retrieved.
    """
    order_value = order_by if order_by else "-created_at"
    finances = (
        finance_model.objects
        .select_related("category")
        .filter(user=user.pk)
        .order_by(order_value)
    )

    try:
        if number_of_items:
            finances = finances[:number_of_items]
            logger.info(
                f"The user [ID: {user.pk}, "
                f"name: {user.email}] successfully received "
                f"a list of last {number_of_items} the users's {finance_model}."
            )
    except IndexError:
        logger.error(
            f"The user [ID: {user.pk}, "
            f"name: {user.email}] - invalid parameter 'number_of_items':"
            f" {number_of_items} - to receive the users's {finance_model}."
        )
        raise InvalidNumberOfItemsError

    return finances

def get_sum_of_finance_in_current_month(
    user: User, finance_model: Union[Type[Incomes], Type[Outcomes]]
) -> float:
    """
    Retrieve total amount of user's incomes or utcomes in the current month.
    If there is no incomes/outcomes in the current month this function returns 0.00.
    """

    current_month = datetime.now().month
    result = (
        get_finance(user=user, finance_model=finance_model)
        .filter(created_at__month=current_month)
        .aggregate(total_sum=Sum("sum"))
    ).get("total_sum")

    if not result:
        logger.info(
            f"The user [ID: {user.pk}, "
            f"name: {user.email}] - there is no {finance_model} in the current month."
        )
        return float(0)

    logger.info(
        f"The user [ID: {user.pk}, "
        f"name: {user.email}] - successfully return a total amount "
        f"of {finance_model} in current month."
    )

    return float(result)
