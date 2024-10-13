from django.contrib.auth import get_user_model
from django.db import models

from api.models.base import BaseDictionary


class Category(BaseDictionary):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Пользователь"
    )
    is_income = models.BooleanField(
        default=True,
        verbose_name="Признак категории дохода"
    )
    is_outcome = models.BooleanField(
        default=False,
        verbose_name="Признак категории расхода"
    )
    is_fixed = models.BooleanField(
        default=True,
        verbose_name="Признак постоянной категории"
    )

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name
