from .base import BaseModel
from django.db import models


class Country(models.Model):
    name = models.CharField(
        max_length=146,
        verbose_name='Краткое название'
    )
    code = models.CharField(
        max_length=3,
        verbose_name='Альфа-2'
    )

    class Meta:
        db_table = "api_countries"
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name

