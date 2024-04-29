from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import (IncomeCategoriesListCreateAPI, IncomeCreateAPI,
                       IncomesRetrieveUpdateDestroyAPI,
                       IncomeSumInCurrentMonthGetAPI,
                       activate_users_api_controller,
                       password_reset_api_controller)

router = DefaultRouter()
urlpatterns = [
    # path(
    #     'categories/',
    #     GetCreateCategoryAPIView.as_view(),
    #     name='categories'
    # ),
    # path(
    #     'income-categories/',
    #     IncomeCategoriesListCreateView.as_view(),
    #     name='income-categories'
    # ),
    # path(
    #     'outcome-categories/',
    #     GetOutcomeCategoriesView.as_view(),
    #     name='outcome-categories'
    # ),
    # path(
    #     'money-box-categories/',
    #     GetMoneyBoxCategoriesView.as_view(),
    #     name='money-box-categories'
    # ),
    # path(
    #     'update-category/<int:pk>',
    #     UpdateCategoryView.as_view(),
    #     name='update-category'
    # ),
    # path(
    #     'del-category/<int:pk>',
    #     DeleteCategoryView.as_view(),
    #     name='del-category'
    # ),
    # path(
    #     'incomecash/',
    #     AddIncomeCashView.as_view(),
    #     name='incomecash'
    # ),
    # path(
    #     'last-5-incomecash/',
    #     Last5IncomeCashView.as_view(),
    #     name='last-5-income-cash'
    # ),
    # path(
    #     'sum-incomecash/',
    #     SumIncomeCashView.as_view(),
    #     name='sum-income-cash'
    # ),
    # path(
    #     'sum-incomecash-group/',
    #     SumIncomeCashGroupView.as_view(),
    #     name='sum-income-cash-group'
    # ),
    # path(
    #     'sum-monthly-income/',
    #     SumMonthlyIncomeView.as_view(),
    #     name='sum-monthly-income'
    # ),
    # path(
    #     'sum-monthly-percent-income/',
    #     SumPercentMonthlyIncomeView.as_view(),
    #     name='sum-percent-monthly-income'
    # ),
    # path(
    #     'update-incomecash/<int:pk>',
    #     UpdateIncomeCashView.as_view(),
    #     name='update-income-cash'
    # ),
    # path(
    #     'delete-incomecash/<int:pk>',
    #     DeleteIncomeCashView.as_view(),
    #     name='delete-income-cash'
    # ),
    # path(
    #     'outcomecash/',
    #     AddOutcomeCashView.as_view(),
    #     name='outcome-cash'
    # ),
    # path(
    #     'last-5-outcomecash/',
    #     Last5OutcomeCashView.as_view(),
    #     name='last-5-outcome-cash'
    # ),
    # path(
    #     'sum-outcomecash/',
    #     SumOutcomeCashView.as_view(),
    #     name='sum-outcome-cash'
    # ),
    # path(
    #     'sum-outcomecash-group/',
    #     SumOutcomeCashGroupView.as_view(),
    #     name='sum-outcome-cash-group'
    # ),
    # path(
    #     'sum-monthly-outcome/',
    #     SumMonthlyOutcomeView.as_view(),
    #     name='sum-monthly-outcome'
    # ),
    # path(
    #     'sum-monthly-percent-outcome/',
    #     SumPercentMonthlyOutcomeView.as_view(),
    #     name='sum-percent-monthly-outcome'
    # ),
    # path(
    #     'update-outcomecash/<int:pk>',
    #     UpdateOutcomeCashView.as_view(),
    #     name='update-outcome-cash'
    # ),
    # path(
    #     'delete-outcomecash/<int:pk>',
    #     DeleteOutcomeCashView.as_view(),
    #     name='delete-outcome-cash'
    # ),
    # path(
    #     'balance/',
    #     BalanceAPIView.as_view(),
    #     name='balance'
    # ),
    # path(
    #     'money-box/',
    #     AddMoneyBoxView.as_view(),
    #     name='money-box'
    # ),
    # path(
    #     'last-5-money-box/',
    #     Last5MoneyBoxView.as_view(),
    #     name='last-5-money-box'
    # ),
    # path(
    #     'sum-money-box/',
    #     SumMoneyBoxView.as_view(),
    #     name='sum-money-box'
    # ),
    # path(
    #     'sum-money-box-group/',
    #     SumMoneyBoxGroupView.as_view(),
    #     name='sum-money-box-group'
    # ),
    # path(
    #     'sum-monthly-money-box/',
    #     SumMonthlyMoneyBoxView.as_view(),
    #     name='sum-monthly-money-box'
    # ),
    # path(
    #     'sum-monthly-percent-money-box/',
    #     SumPercentMonthlyMoneyBoxView.as_view(),
    #     name='sum-percent-monthly-money-box'
    # ),
    # path(
    #     'update-money-box/<int:pk>',
    #     UpdateMoneyBoxView.as_view(),
    #     name='update-money-box'
    # ),
    # path(
    #     'delete-money-box/<int:pk>',
    #     DeleteMoneyBoxView.as_view(),
    #     name='delete-money-box'
    # ),
    # path(
    #     'ai-answer/',
    #     RequestDataAIView.as_view(),
    #     name='ai-answer'
    # ),
    # path(
    #     'tax_deduction/',
    #     AIAnswerTaxDeductionView.as_view(),
    #     name='tax-deduction'
    # ),
    # path(
    #     'saving_money_advice/',
    #     AIAnswerSavingMoneyAdvice.as_view(),
    #     name='saving-money-advice'
    # ),
    # path('report/', ReportAPIView.as_view(), name='report'),
    path("auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("activate/", activate_users_api_controller, name="activate-users"),
    path(
        "password/reset/confirm/", password_reset_api_controller, name="reset-password"
    ),
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
    path(
        "incomes_in_current_month/",
        IncomeSumInCurrentMonthGetAPI.as_view(),
        name="income-sum-in-current-month",
    ),
    # path('api/get-users/', GetUsers.as_view(), name='get-users'),
    # path('api/', include(router.urls)),
    # path('api/registration/', CreateUser.as_view(), name='create-user'),
    # path('api/drf-auth/', include('rest_framework.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
