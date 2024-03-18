from django.db import models
from .common import CommonCategory, CommonSumInfo


class IncomeCategories(CommonCategory):
    """Describes the fields and attributes of the IncomeCategories model in the database."""

    pass


class Incomes(CommonSumInfo):
    """Describes the fields and attributes of the Incomes model in the database."""
    
    category = models.ForeignKey(
        IncomeCategories,
        on_delete=models.CASCADE
    )
