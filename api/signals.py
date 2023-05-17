from django.db.models.signals import pre_delete
from django.dispatch import receiver

from api.models import MoneyBox, OutcomeCash


@receiver(pre_delete, sender=MoneyBox)
# Сигнал pre_delete удаляет все записи, связанные с MoneyBox из OutcomeCash,
# при условии box_sum < box_target

def delete_related_outcome_cash(sender, instance, **kwargs):
    if instance.box_sum < instance.box_target:
        OutcomeCash.objects.filter(user=instance.user, categories_id=instance.categories_id).delete()
