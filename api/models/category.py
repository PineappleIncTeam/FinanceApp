from django.contrib.auth import get_user_model
from django.db import models

from .base import BaseDictionary


class Category(BaseDictionary):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Пользователь",
    )
    is_income = models.BooleanField(
        default=True, verbose_name="Признак категории дохода"
    )
    is_outcome = models.BooleanField(
        default=False, verbose_name="Признак категории расхода"
    )
    is_visibility = models.BooleanField(
        default=True, verbose_name="Признак видимости категории"
    )
    is_system = models.BooleanField(
        default=False, verbose_name="Признак системной категории"
    )

    class Meta:
        db_table = "categories"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    # Проверка системной категории
    def is_system_category(self):
        return self.is_system

    # Проверка видимости категории
    def is_visible(self):
        return self.is_visibility

    def save(self, *args, **kwargs):
        if self.pk and self.is_system:
            raise ValueError("System categories cannot be edited.")
        super(Category, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_system:
            raise ValueError("System categories cannot be deleted.")
        super(Category, self).delete(*args, **kwargs)