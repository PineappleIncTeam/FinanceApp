from .base import BaseModel
from django.db import models


class Countries(BaseModel):
    code = models.CharField(
        max_length=4,
        verbose_name='Код страны'
    )
    name = models.CharField(
        max_length=56,
        verbose_name='Краткое название'
    )
    full_name = models.CharField(
        max_length=56,
        verbose_name='Полное название',

    )
    alfa2 = models.CharField(
        max_length=2,
        verbose_name='Aльфа-2'
    )
    alfa3 = models.CharField(
        max_length=3,
        verbose_name='Aльфа-3'
    )

    class Meta:
        db_table = "api_countries"

    def __str__(self):
        return self.name

