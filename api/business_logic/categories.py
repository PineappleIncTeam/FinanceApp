from __future__ import annotations
from typing import TYPE_CHECKING
from api.models import IncomeCategories

if TYPE_CHECKING:
    from api.models import User
    from django.db.models import QuerySet


def get_income_categories(user: User) -> QuerySet:
    """
    Retrieve all user's incomes categories.
    Args:
        user (User): The instance of User model whose incomes are to be retrieved.
    Returns:
        QuerySet of users's incomes categories.
    """

    user_id = user.pk
    query_result = IncomeCategories.objects.prefetch_related("incomes_set").filter(
            incomes__user=user_id,
            incomes__is_hidden=False
    ).distinct("incomes__category")

    return query_result
