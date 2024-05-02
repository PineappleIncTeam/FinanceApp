from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from api.views import (
    IncomeCategoriesListCreateAPI,
    IncomesRetrieveUpdateDestroyAPI,
    IncomeSumInCurrentMonthGetAPI,
    LastIncomesGetAPI,
)


from api.views import (
    activate_users_api_controller,
    password_reset_api_controller,
)

router = DefaultRouter()
urlpatterns = [
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('activate/', activate_users_api_controller, name="activate-users"),
    path(
        'password/reset/confirm/',
        password_reset_api_controller,
        name="reset-password"
    ),
    path(
        'income_categories/',
        IncomeCategoriesListCreateAPI.as_view(),
        name='income-categories'
    ),
    path(
        'income/<int:pk>/',
        IncomesRetrieveUpdateDestroyAPI.as_view(),
        name='income-info'
    ),
    path(
        'last_incomes/',
        LastIncomesGetAPI.as_view(),
        name='get-last-incomes'
    ),
    path(
        'incomes_in_current_month/',
        IncomeSumInCurrentMonthGetAPI.as_view(),
        name='income-sum-in-current-month'
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
