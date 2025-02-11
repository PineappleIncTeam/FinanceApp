from django.db import models


class CurrencyData(models.Model):
    currency = models.CharField(max_length=10, unique=True, verbose_name="Связка валют")
    rate = models.DecimalField(max_digits=20, decimal_places=10, verbose_name="Значение курса")

    def __str__(self):
        return self.name
