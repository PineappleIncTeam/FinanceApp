from django.contrib import admin
from .models import User, AbstractCash, Categories, IncomeCash, OutcomeCash, MoneyBox

# Register your models here.
admin.site.register(
    (
        User,
        Categories,
        IncomeCash,
        OutcomeCash,
        MoneyBox,)
)
