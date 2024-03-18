from django.db import models
from django.contrib.auth import get_user_model

from .base import BaseModel


class Targets(BaseModel):
    """Describes the fields and attributes of the Targets model in the database."""

    target_name = models.CharField(
        max_length=200,
    )
    target_sum = models.DecimalField(
        max_digits=19,
        decimal_places=2
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    is_hidden = models.BooleanField(
        default=False
    )


class Accumulations(BaseModel):
    """Describes the fields and attributes of the Accumulations model in the database."""
    
    target = models.ForeignKey(
        Targets,
        on_delete=models.CASCADE
    )
    sum = models.DecimalField(
        max_digits=19,
        decimal_places=2,
    )
