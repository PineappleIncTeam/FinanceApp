from django.contrib import admin
from api.models import User, Categories, IncomeCash, OutcomeCash, MoneyBox


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email',)
    ordering = ('email',)


admin.site.register(
    (
        Categories,
        IncomeCash,
        OutcomeCash,
        MoneyBox,)
)
