from django.contrib import admin
from .models import User, Category, IncomeCash, OutcomeCash, MoneyBox

admin.site.register(
    (
        User,
        Category,
        IncomeCash,
        OutcomeCash,
        MoneyBox,)
)
