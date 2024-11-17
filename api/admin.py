from django.contrib import admin
from django.contrib.auth import get_user_model

from api.models.countries import Country

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email',)
    ordering = ('email',)
    search_fields = ('username', 'email',)


admin.site.register(
    Country
)
