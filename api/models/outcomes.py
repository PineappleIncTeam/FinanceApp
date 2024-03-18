from django.db import models
from .common import CommonCategory, CommonSumInfo


class OutcomeCategories(CommonCategory):
    """Describes the fields and attributes of the OutcomeCategories model in the database."""

    pass


class Outcomes(CommonSumInfo):
    """Describes the fields and attributes of the Outcomes model in the database."""

    category = models.ForeignKey(
        OutcomeCategories,
        on_delete=models.CASCADE
    )
