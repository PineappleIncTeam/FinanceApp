from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path

from api.views import (AccumulationCreateAPI,
                       AccumulationRetrieveUpdateDestroyAPI,
                       AccumulationsCategoriesArchiveAPI,
                       AccumulationsCategoriesInfoAPI,
                       AccumulationsCategoriesListCreateAPI,
                       AccumulationsInfoGetAPI, BalanceGetAPI,
                       CustomTokenCreateAPI, IncomeCategoriesListCreateAPI,
                       IncomeCreateAPI, IncomesRetrieveUpdateDestroyAPI,
                       IncomeSumInCurrentMonthGetAPI, LastAccumulationsGetAPI,
                       LastIncomesGetAPI, LastOutcomesGetAPI,
                       OperationListCreateAPI,
                       OperationRetrieveUpdateDestroyAPI,
                       OutcomeCategoriesListCreateAPI,
                       OutcomeRetrieveUpdateDestroyView,
                       OutcomeSumInCurrentMonthGetAPI,
                       TotalAmountAccumulationsGetAPI,
                       activate_users_api_controller,
                       password_reset_api_controller)

urlpatterns = [
    path("auth/token/login/", CustomTokenCreateAPI.as_view(), name="login"),
    path("auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("activate/", activate_users_api_controller, name="activate-users"),
    path("password/reset/confirm/", password_reset_api_controller, name="reset-password"),
    # BALANCE
    path("balance/", BalanceGetAPI.as_view(), name="balance"),
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
    path("outcomes/<int:pk>/", OutcomeRetrieveUpdateDestroyView.as_view(), name="change-outcomes"),
    # ACCUMULATIONS
    path(
        "total_amount_of_accumulations/",
        TotalAmountAccumulationsGetAPI.as_view(),
        name="total-amount-of-accumulations",
    ),
    path(
        "accumulation_categories/",
        AccumulationsCategoriesListCreateAPI.as_view(),
        name="accumulation-categories",
    ),
    path(
        "accumulation_categories/<int:pk>/",
        AccumulationsCategoriesInfoAPI.as_view(),
        name="accumulation-category-info",
    ),
    path(
        "archive_accumulation_category/<int:pk>/",
        AccumulationsCategoriesArchiveAPI.as_view(),
        name="archive-accumulation-category",
    ),
    path(
        "accumulation/<int:pk>/",
        AccumulationRetrieveUpdateDestroyAPI.as_view(),
        name="accumulation-info",
    ),
    path("accumulation/", AccumulationCreateAPI.as_view(), name="add-accumulation"),
    path("last_accumulations/", LastAccumulationsGetAPI.as_view(), name="get-last-accumulations"),
    path("accumulations_info/", AccumulationsInfoGetAPI.as_view(), name="all-accumulations-info"),
    path("operations/", OperationListCreateAPI.as_view(), name="operations-list-create"),
    path(
        "operations/<int:pk>/",
        OperationRetrieveUpdateDestroyAPI.as_view(),
        name="operations-detail"
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
