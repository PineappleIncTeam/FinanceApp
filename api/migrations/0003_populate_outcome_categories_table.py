"""
Custom migration that populate OutcomeCategories table with default values.
"""

from typing import Any

from django.db import migrations


DEFAULT_OUTCOME_CATEGORIES = (
    "еда",
    "одежда",
    "жилищно-коммунальные услуги",
    "развлечения",
    "внезапная покупка",
)


def populate_outcome_categories_table(apps: Any, schema_editor: Any) -> None:
    """Populates table with default values."""
    outcome_categories = apps.get_model('api', 'OutcomeCategories')
    outcome_categories_list = [outcome_categories(name=category) for category in DEFAULT_OUTCOME_CATEGORIES]
    outcome_categories.objects.bulk_create(outcome_categories_list, ignore_conflicts=True)


def reverse_outcome_categories_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""
    outcome_categories = apps.get_model('api', 'OutcomeCategories')

    for category in DEFAULT_OUTCOME_CATEGORIES:
        outcome_categories.objects.get(name=category).delete()


class Migration(migrations.Migration):
    """Creates django migration that writes data to the database."""

    dependencies = [
        ("api", "0002_populate_income_categories_table"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_outcome_categories_table,
            reverse_code=reverse_outcome_categories_table_population,
        )
    ]
