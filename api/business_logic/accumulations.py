from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from django.db.models import Sum

from api.models import Accumulations

if TYPE_CHECKING:
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
        f"name: {user.email}] - successfully return a total amount "
        f"of accumulations on current date {current_date}."
    )

    return float(result)
