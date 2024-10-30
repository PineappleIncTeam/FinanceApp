from django.db import models
from api.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField()
    email = models.CharField(max_length=30, null=True)
    country = models.CharField(max_length=146, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        """Describes class metadata."""

        db_table = "profiles"

