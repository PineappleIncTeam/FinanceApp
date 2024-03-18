"""
Custom migration that populate OutcomeCategories table with default values.
"""

from typing import Any

from api.models import OutcomeCategories
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

    outcome_categories_list = [OutcomeCategories(name=category) for category in DEFAULT_OUTCOME_CATEGORIES]
    OutcomeCategories.objects.bulk_create(outcome_categories_list, ignore_conflicts=True)


def reverse_outcome_categories_table_population(apps: Any, schema_editor: Any) -> None:
    """Reverse table population."""

    for category in DEFAULT_OUTCOME_CATEGORIES:
        OutcomeCategories.objects.get(name=category).delete()


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
