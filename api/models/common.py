from django.db import models
from django.contrib.auth import get_user_model
from enum import Enum

from .base import BaseModel


class CommonCategory(BaseModel):
    """
    Describes common fields and attributes of the IncomeCategories
    and OutcomeCategories models in the database.
    """

    name = models.CharField(unique=True, max_length=200)

    class Meta:
        """Describes class metadata."""

        abstract = True


class CategoryType(Enum):
    """
    Determine types of incomes and outcomes.
    """

    CONSTANT = 'constant'
    TEMPORARY = "temporary"

    @staticmethod
    def choices():
        return (
            (CategoryType.CONSTANT.value, "constant"),
            (CategoryType.TEMPORARY.value, "temporary"),
        )


class CommonSumInfo(BaseModel):
    """
    Describes common fields and attributes of the Incomes
    and Outcomes models in the database.
    """
    
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    sum = models.DecimalField(
        max_digits=19,
        decimal_places=2
    )
    type = models.CharField(
        choices=CategoryType.choices()
    )
    is_hidden = models.BooleanField(
        default=False
    )

    class Meta:
        """Describes class metadata."""

        abstract = True
