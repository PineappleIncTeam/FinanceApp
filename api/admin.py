from django.contrib import admin
from .models import User, Categories, IncomeCash, OutcomeCash, MoneyBox

admin.site.register(
    (
        User,
        Categories,
        IncomeCash,
        OutcomeCash,
        MoneyBox,)
)
