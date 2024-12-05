from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Category, User


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        default_categories = [
            {"name": "Продукты", "is_income": False, "is_outcome": True},
            {"name": "Одежда", "is_income": False, "is_outcome": True},
            {"name": "Развлечения", "is_income": False, "is_outcome": True},
            {"name": "ЖКХ", "is_income": False, "is_outcome": True},
            {"name": "Зарплата", "is_income": True, "is_outcome": False},
        ]

        for category_data in default_categories:
            Category.objects.create(user=instance, **category_data)

        # Create system category "из накоплений"
        Category.objects.create(
            user=instance,
            name="из накоплений",
            is_income=False,
            is_outcome=True,
            is_visibility=False,
            is_system=True,
        )