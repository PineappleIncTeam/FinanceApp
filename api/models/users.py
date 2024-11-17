from __future__ import annotations

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import SET_NULL
from django.utils.html import escape
from django.utils.translation import gettext as _
from select import select

from .base import BaseModel
from .countries import Country


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
        Profile.objects.create(user=user)
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
    """
    Describes the fields and attributes of the User model in the database.
    """

    email = models.EmailField(unique=True)
    username = models.CharField(
        blank=True,
        null=True,
        default="Пользователь FinanceApp"
    )

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        """Describes class metadata."""

        db_table = "users"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=10, null=True, choices=[('M', 'Male'), ('F', 'Female')])
    country = models.ForeignKey(Country, on_delete=SET_NULL, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} Profile'