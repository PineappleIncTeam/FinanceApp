from random import choices

from django.db import models
from django.db.models import SET_NULL

import os
import uuid

from .countries import Country
from .users import User

DEFAULT_TYPES = [
    (0, "not default"),
    (1, "default 1"),
    (2, "default 2"),
    (3, "default 3"),
    (4, "default 4"),
    (5, "default 5"),
    (6, "default 6"),
    (7, "default 7"),
    (8, "default 8"),
]

def upload_to(instance, filename):
    ext = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("avatars/", unique_filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=10, choices=[("M", "Male"), ("F", "Female")], null=True)
    country = models.ForeignKey(Country, on_delete=SET_NULL, null=True)
    avatar = models.ImageField(upload_to=upload_to, null=True, blank=True)
    default = models.IntegerField(choices=DEFAULT_TYPES, null=False, default=0)

    def __str__(self):
        return f"{self.nick_name} Profile"