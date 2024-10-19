from .base import BaseModel
from django.db import models


class Countries(models.Model):
    code = models.CharField(
        max_length=4,
        verbose_name='Код страны'
    )
    name = models.CharField(
        max_length=146,
        verbose_name='Краткое название'
    )
    full_name = models.CharField(
        max_length=146,
        verbose_name='Полное название',

    )

    class Meta:
        db_table = "api_countries"

    def __str__(self):
        return self.name

