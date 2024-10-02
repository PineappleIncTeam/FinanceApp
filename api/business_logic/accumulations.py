from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from django.db.models import Sum

from api.models import Accumulations, Targets

from .errors import InvalidNumberOfItemsError

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from api.models import User


logger = logging.getLogger(__name__)


def get_total_amount_of_accumulations_on_the_current_date(
    user: User,
    date: datetime
) -> float:
    """
    Retrieve total amount of user's acumulations in the current date.
    If there is no iacumulations on the current date this function
    returns 0.00.
    """

    current_date = date if date else datetime.now()
    result = (
        Accumulations.objects
        .prefetch_related("accumulations_set")
        .filter(target__user=user, created_at__lte=current_date)
        .aggregate(total_sum=Sum("sum"))
    ).get("total_sum")

    if not result:
        logger.info(
            f"The user [ID: {user.pk}, "
            f"name: {user.email}] - there is no accumulation "
            f"on the current date {current_date}."
        )
        return float(0)

    logger.info(
        f"The user [ID: {user.pk}, "
        f"name: {user.email}] - successfully return a total amount of accumulations."
    )

    return float(result)


def get_accumulations(
    user: User,
    order_by: Optional[str] = None,
    number_of_items: Any = None
) -> QuerySet[Accumulations]:
    """
    Retrieve all user's accumulations.

    Args:
        order_by (str | None): Condition for ordering
        number_of_items (int | None): An amount of objects
        are to be retrieved.
    """

    order_value = order_by if order_by else "-created_at"
    finances = (
        Accumulations.objects
        .select_related("target")
        .filter(target__user=user.pk, target__is_hidden=False)
        .order_by(order_value)
    )
    try:
        if number_of_items:
            items = int(number_of_items)
            finances = finances[:items]
            logger.info(
                f"The user [ID: {user.pk}, "
                f"name: {user.email}] successfully received "
                f"a list of last {number_of_items} accumulations"
            )

    except IndexError:
        logger.error(
            f"The user [ID: {user.pk}, "
            f"name: {user.email}] - invalid parameter 'number_of_items':"
            f" {number_of_items} - to receive the users's accumulations."
        )
        raise InvalidNumberOfItemsError("Invalid parameter items in query parameters.")

    except ValueError:
        raise InvalidNumberOfItemsError("Invalid parameter items in query parameters.")

    return finances


def get_accumulation_info(user: User) -> QuerySet[Targets]:
    """
    To get total information about all user's accumulations.
    """

    result = Targets.objects.filter(
        user=user, is_hidden=False
    ).prefetch_related(
        "accumulations_set"
    ).annotate(
        total_sum=Sum("accumulations__sum")
    ).values(
        "target_name", "target_sum", "total_sum"
    )

    logger.info(
        f"name: {user.email}] - successfully return a total amount "
        f"of accumulations on current date."
    )

    return float(result)
