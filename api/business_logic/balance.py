from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from api.business_logic import (
    get_sum_of_finance_on_current_date,
    get_total_amount_of_accumulations_on_the_current_date)
from api.models import Incomes, Outcomes

if TYPE_CHECKING:
    from api.models import User


logger = logging.getLogger(__name__)


def get_balance(user: User, date: datetime) -> float:
    """
    To get user's balance on the current date.
    """

    incomes_sum = get_sum_of_finance_on_current_date(
        user=user,
        finance_model=Incomes,
        date=date
    )
    outcomes_sum = get_sum_of_finance_on_current_date(
        user=user,
        finance_model=Outcomes,
        date=date
    )

    accumulations_sum = get_total_amount_of_accumulations_on_the_current_date(
        user=user,
        date=date
    )

    balance = incomes_sum - outcomes_sum - accumulations_sum

    logger.info(
        f"The user [ID: {user.pk}, "
        f"name: {user.email}] - successfully return a balance "
        f"on the current date {date}."
    )

    return balance
