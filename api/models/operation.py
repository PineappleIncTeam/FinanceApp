from django.contrib.auth import get_user_model
from django.db import models

from api.models import Category, Target
from api.models.base import BaseModel

INCOME_CATEGORY = "income"
OUTCOME_CATEGORY = "outcome"

OPERATION_TYPES = [
    (INCOME_CATEGORY, "Категория доходов"),
    (OUTCOME_CATEGORY, "Категория расходов"),
]


class Operation(BaseModel):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    type = models.CharField(
        max_length=10,
        choices=OPERATION_TYPES,
    )
    categories = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="operations",
        null=True
    )
    target = models.ForeignKey(
        Target,
        on_delete=models.CASCADE,
        verbose_name="Цель",
        related_name="operations",
        null=True
    )
    amount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        verbose_name="Сумма"
    )
    date = models.DateField(verbose_name="Дата записи")

    class Meta:
        db_table = "operations"

    def __str__(self):
        return f"{self.categories} {self.date}"
