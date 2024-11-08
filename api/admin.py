from django.contrib import admin
from django.contrib.auth import get_user_model # Categories, IncomeCash, OutcomeCash, MoneyBox

from api.models.countries import Country


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email',)
    ordering = ('email',)
    search_fields = ('username', 'email',)


# admin.site.register(
#     (
#         Categories,
#         IncomeCash,
#         OutcomeCash,
#         MoneyBox,)
# )

admin.site.register(
    Country
)
