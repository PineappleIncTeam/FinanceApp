from datetime import datetime

from django.db import models


class BaseModel(models.Model):
    """Describes the fields and attributes of the Base model in the database."""

    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Describes class metadata."""

        abstract = True
