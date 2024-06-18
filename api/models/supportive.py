from django.db import models


class Country(models.Model):
    """List of countries where the user may be located"""

    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class City(models.Model):
    """List of cities where the user may be located"""

    name = models.CharField(max_length=32)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
