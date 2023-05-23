from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import MoneyBox, OutcomeCash


@receiver(pre_delete, sender=MoneyBox)
def delete_related_outcome_cash(sender, instance, **kwargs):
    outcome_cash = OutcomeCash.objects.filter(user=instance.user, categories=instance.categories)
    if outcome_cash:
        outcome_cash.delete()
