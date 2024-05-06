from django.contrib.auth import get_user_model
from django.db import models

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


class CommonSumInfo(BaseModel):
    """
    Describes common fields and attributes of the Incomes
    and Outcomes models in the database.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    sum = models.DecimalField(max_digits=19, decimal_places=2)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        """Describes class metadata."""

        abstract = True
