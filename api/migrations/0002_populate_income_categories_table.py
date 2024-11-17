"""
Custom migration that populate IncomeCategories table with default values.
"""

from typing import Any

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
    income_categories = apps.get_model("api", "IncomeCategories")
    income_categories_list = [income_categories(name=category) for category in DEFAULT_INCOME_CATEGORIES]
    income_categories.objects.bulk_create(income_categories_list, ignore_conflicts=True)


def reverse_income_categories_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    income_categories = apps.get_model("api", "IncomeCategories")

    for category in DEFAULT_INCOME_CATEGORIES:
        income_categories.objects.get(name=category).delete()


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
