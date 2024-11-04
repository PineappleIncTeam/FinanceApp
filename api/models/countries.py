from .base import BaseModel
from django.db import models


class Country(models.Model):
    name = models.CharField(
        max_length=146,
        verbose_name='Краткое название'
    )
    full_name = models.CharField(
        max_length=146,
        verbose_name='Полное название',

    )
    alfa2 = models.CharField(
        max_length=3,
        verbose_name='Альфа-2'
    )

    class Meta:
        db_table = "api_countries"

    def __str__(self):
        return self.name

