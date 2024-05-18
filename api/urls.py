from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import (CustomTokenCreateAPI, IncomeCategoriesListCreateAPI,
                       IncomeCreateAPI, IncomesRetrieveUpdateDestroyAPI,
                       IncomeSumInCurrentMonthGetAPI, LastIncomesGetAPI,
                       LastOutcomesGetAPI, OutcomeCategoriesListCreateAPI,
                       OutcomeSumInCurrentMonthGetAPI,
                       activate_users_api_controller,
                       password_reset_api_controller)

router = DefaultRouter()
urlpatterns = [
    path("auth/token/login/", CustomTokenCreateAPI.as_view(), name="login"),
    path("auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("activate/", activate_users_api_controller, name="activate-users"),
    path("password/reset/confirm/", password_reset_api_controller, name="reset-password"),
    # INCOMES
    path(
        "income_categories/",
        IncomeCategoriesListCreateAPI.as_view(),
        name="income-categories",
    ),
    path(
        "income/<int:pk>/",
        IncomesRetrieveUpdateDestroyAPI.as_view(),
        name="income-info",
    ),
    path("income/", IncomeCreateAPI.as_view(), name="add-income"),
    path("last_incomes/", LastIncomesGetAPI.as_view(), name="get-last-incomes"),
    path(
        "incomes_in_current_month/",
        IncomeSumInCurrentMonthGetAPI.as_view(),
        name="income-sum-in-current-month",
    ),
    # OUTCOMES
    path(
        "outcomes_in_current_month/",
        OutcomeSumInCurrentMonthGetAPI.as_view(),
        name="outcome-sum-in-current-month",
    ),
    path("last_outcomes/", LastOutcomesGetAPI.as_view(), name="get-last-outcomes"),
    path(
        "outcome_categories/",
        OutcomeCategoriesListCreateAPI.as_view(),
        name="outcome-categories",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
