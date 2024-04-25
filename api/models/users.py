from __future__ import annotations
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.html import escape
from django.utils.translation import gettext as _

from typing import Optional

from .base import BaseModel


class CustomUserManager(UserManager):

    def create_user(self, email: str, password=None, **extra_fields) -> User:
        """Create a new user profile"""

        if not email:
            raise ValueError(_('User must have an email address'))

        user_email: str = self.normalize_email(email)
        user: User = self.model(email=user_email, **extra_fields)
        password = escape(password)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class User(BaseModel, AbstractUser):
    '''
    Describes the fields and attributes of the User model in the database.
    '''

    email = models.EmailField(unique=True)
    username = models.CharField(
        blank=True,
        null=True,
        default="Пользователь FinanceApp"
    )

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[Optional[str]] = []

    class Meta:
        """Describes class metadata."""

        db_table = "users"
