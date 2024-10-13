from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseDictionary(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name="Наименование"
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="Признак удаления записи"
    )

    class Meta:
        abstract = True
