from __future__ import annotations
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union
from api.models import Incomes
from .errors import InvalidNumberOfItems

from django.db.models import Sum


if TYPE_CHECKING:
    from django.db.models import QuerySet
    from api.models import User


logger = logging.getLogger(__name__)


def get_incomes(
        user: User,
        order_by: Optional[str] = None,
        number_of_items: Optional[int] = None
) -> QuerySet:
    """
    Retrieve all user's incomes.
    Args:
        user (User): The instance of User model whose incomes are to be retrieved.
        order_by (str | None): Condition for ordering
        number_of_items (int | None): An amount of objects are to be retrieved.
    Returns:
        QuerySet of users's incomes.
    """

    if not order_by:
        user_incomes = Incomes.objects.filter(user=user.pk)
    else:
        user_incomes = Incomes.objects.filter(user=user.pk).order_by(order_by)

    try:
        if number_of_items:
            user_incomes = user_incomes[:number_of_items]
            logger.info(
            f"The user [ID: {user.pk}, "
            f"name: {user.email}] successfully received "
            f"a list of last {number_of_items} the users's Incomecategories."
            )
    except IndexError:
        logger.error(
            f"The user [ID: {user.pk}, "
            f"name: {user.email}] - invalid parameter 'number_of_items':"
            f" {number_of_items} - to receive the users's Incomecategories."
            )
        raise InvalidNumberOfItems
    
    return user_incomes


def get_sum_of_incomes_in_current_month(user: User) -> Union[float, str]:
    """
    Retrieve total amount of yser's incomes in the current month.
    Args:
        user (User): The instance of User model whose incomes are to be retrieved.
    Returns:
        An amount of user's incomes in the current month. If there is no income in the current month
        this function returns the string "0.00".
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
        return "0.00"
    
    logger.info(
        f"The user [ID: {user.pk}, "
        f"name: {user.email}] - successfully return a total amount "
        f"of incomes in current month."
    )
    
    return result
