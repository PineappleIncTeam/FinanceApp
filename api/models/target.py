from django.contrib.auth import get_user_model
from django.db import models

from .base import BaseDictionary


class Target(BaseDictionary):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        verbose_name="Целевая сумма"
    )

    class Meta:
        db_table = "targets"

    def __str__(self):
        return self.name
