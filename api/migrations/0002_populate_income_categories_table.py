"""
Custom migration that populate IncomeCategories table with default values.
"""

from typing import Any

from api.models import IncomeCategories
from django.db import migrations


DEFAULT_INCOME_CATEGORIES = (
    "зарплата",
    "подработка",
    "пассивный доход",
    "наследство",
    "из накоплений",
)


def populate_income_categories_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""

    income_categories_list = [IncomeCategories(name=category) for category in DEFAULT_INCOME_CATEGORIES]
    IncomeCategories.objects.bulk_create(income_categories_list, ignore_conflicts=True)


def reverse_income_categories_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""

    for category in DEFAULT_INCOME_CATEGORIES:
        IncomeCategories.objects.get(name=category).delete()


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_income_categories_table,
            reverse_code=reverse_income_categories_table_population,
        )
    ]
