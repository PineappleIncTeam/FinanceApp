from django.contrib.auth import password_validation
from django.db import models
from django.contrib.auth.models import AbstractUser

from .base import BaseModel


class User(BaseModel, AbstractUser):
    '''Describes the fields and attributes of the User model in the database.'''
    
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    class Meta:
        """Describes class metadata."""

        db_table = "users"
