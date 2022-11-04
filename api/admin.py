from django.contrib import admin
from .models import User, AbstractCash, Categories, IncomeCash, OutcomeCash, MoneyBox

# Register your models here.
admin.site.register(
    (
        User,
        AbstractCash,
        Categories,
        IncomeCash,
        OutcomeCash,
        MoneyBox,)
)
