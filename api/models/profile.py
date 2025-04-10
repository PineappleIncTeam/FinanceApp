from django.db import models
from django.db.models import SET_NULL

import os
import uuid

from .countries import Country
from .users import User

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

    def __str__(self):
        return f"{self.nick_name} Profile"