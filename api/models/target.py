from django.contrib.auth import get_user_model
from django.db import models

from .base import BaseDictionary

IN_PROGRESS = "in_progress"
ACHIEVED = "achieved"

STATUS_TYPES = [
    (IN_PROGRESS, "В процессе"),
    (ACHIEVED, "Достигнута"),
]


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
    status = models.CharField(
        default=IN_PROGRESS,
        choices=STATUS_TYPES,
        max_length=15,
        verbose_name="Статус цели"
    )
    current_sum = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        default=0,
        verbose_name="Текущая сумма"
    )

    class Meta:
        db_table = "targets"

    def __str__(self):
        return self.name
