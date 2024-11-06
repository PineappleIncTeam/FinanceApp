from __future__ import annotations

import logging
from typing import Optional

from django.db.models import QuerySet

from api.models import User, Category

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

    query_result = Category.objects.filter(
        user=user.pk
    )

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
