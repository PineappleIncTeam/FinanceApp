import logging
from datetime import date, datetime, timedelta
from typing import Any, Optional

from django.db import transaction
from django.db.models import Case, DecimalField, F, Q, QuerySet, Sum, Value, When
from django.db.models.functions import TruncMonth
from rest_framework.exceptions import ValidationError

from api.models import TARGETS, Category, Operation, Target, User
from api.models.operation import INCOME_CATEGORY, OUTCOME_CATEGORY
from FinanceBackend.settings import DEFAULT_DATE_FORMAT_STR, DEFAULT_MONTH_FORMAT_STR

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

    filters = {"user": user.pk}
    if is_income is not None:
        filters["is_income"] = is_income
    if is_outcome is not None:
        filters["is_outcome"] = is_outcome
    if is_deleted is not None:
        filters["is_deleted"] = is_deleted


    query_result = Category.objects.filter(**filters)

    logger.info(
        "The user [ID: %s, name: %s] successfully received a list of the users's categories.",
        user.pk,
        user.email
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
    ).order_by("-status", "name")

    logger.info(
        "The user [ID: %s, name: %s] successfully received a list of the users's targets.",
        user.pk,
        user.email
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
            type=TARGETS,
            categories=category[0],
            amount=target.current_sum,
            date=date.today()
        )
    return returned_operation


def get_first_day_of_current_month() -> date:
    return date.today().replace(day=1)


def get_last_day_of_current_month() -> date:
    start_of_next_month = get_first_day_of_current_month()
    if start_of_next_month.month == 12:
        start_of_next_month = date(start_of_next_month.year + 1, 1, 1)
    else:
        start_of_next_month = date(start_of_next_month.year, start_of_next_month.month + 1, 1)

    return start_of_next_month - timedelta(days=1)


def convert_str_to_date(date_str: str) -> date:
    try:
        return datetime.strptime(date_str, DEFAULT_DATE_FORMAT_STR).date()
    except ValueError:
        raise ValidationError("Invalid date format. Use YYYY-MM-DD.")


def get_category_report_data(
    operation_type: str, end_date: date, start_date: date
) -> dict[int, dict[str, Any]]:
    operations = (
        Operation.objects
        .select_related("categories")
        .filter(
            type=operation_type,
            date__range=[start_date, end_date],
            categories__isnull=False,
        ).filter(
            ~Q(categories__is_income=False, categories__is_outcome=False)
        )
    )

    aggregated_data = operations.annotate(
        month=TruncMonth("date")
    ).values("categories__id", "categories__name", "month").annotate(
        total=Sum("amount")
    ).order_by("month")
    results = {}
    for entry in aggregated_data:
        category_id = entry["categories__id"]
        category_name = entry["categories__name"]
        month = entry["month"].strftime(DEFAULT_MONTH_FORMAT_STR)
        amount = entry["total"]

        if category_id not in results:
            results[category_id] = {
                "category_id": category_id,
                "category_name": category_name,
                "amount": 0,
                "items": []
            }

        results[category_id]["amount"] += amount
        results[category_id]["items"].append({
            "month": month,
            "amount": amount
        })

    return results


def get_and_check_date_params(start_date_str: str, end_date_str: str) -> tuple:
    if start_date_str and not end_date_str or not start_date_str and end_date_str:
        raise ValidationError("Both start and end dates must be provided.")

    if not start_date_str or not end_date_str:
        start_date = get_first_day_of_current_month()
        end_date = get_last_day_of_current_month()
    else:
        start_date = convert_str_to_date(start_date_str)
        end_date = convert_str_to_date(end_date_str)
        if start_date > end_date:
            raise ValidationError("Start date must be before end date.")

    return start_date, end_date


def get_summary_data(user, start_date=None, end_date=None):
    data = (
        Operation.objects
        .filter(user=user)
        .select_related("categories", "target")
    )

    if start_date and end_date:
        data = data.filter(
            date__range=[start_date, end_date]
        )

    return data.aggregate(
        total_expenses=Sum(
            Case(
                When(
                    Q(type=OUTCOME_CATEGORY) | Q(type=TARGETS, categories__id=None),
                    then=F("amount")
                ),
                default=Value(0),
                output_field=DecimalField()
            )
        ),
        total_income=Sum(
            Case(
                When(categories__isnull=False, type=INCOME_CATEGORY, then=F("amount")),
                default=Value(0),
                output_field=DecimalField()
            )
        ),
        total_savings=Sum(
            Case(
                When(target__isnull=False, then=F("amount")),
                default=Value(0),
                output_field=DecimalField()
            )
        ),
    )
