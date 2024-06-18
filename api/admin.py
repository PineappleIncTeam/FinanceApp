from django.contrib import admin
from django.contrib.auth import (
    get_user_model,
)  # Categories, IncomeCash, OutcomeCash, MoneyBox
from api.models import Country, City


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
    )
    ordering = ("email",)
    search_fields = (
        "username",
        "email",
    )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "country",
    )
    ordering = ("name",)
    search_fields = (
        "name",
        "country__name",
    )
    list_filter = ("country",)


# admin.site.register(
#     (
#         Categories,
#         IncomeCash,
#         OutcomeCash,
#         MoneyBox,)
# )
