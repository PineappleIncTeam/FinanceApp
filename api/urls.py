from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

urlpatterns = [
    path('categories/', GetCreateCategoryAPIView.as_view(), name='categories'),
    path('income-categories/', GetIncomeCategories.as_view(), name='income-categories'),
    path('outcome-categories/', GetOutcomeCategories.as_view(), name='outcome-categories'),
    path('money-box-categories/', GetMoneyBoxCategories.as_view(), name='money-box-categories'),
    path('update-category/<int:pk>', UpdateCategory.as_view(), name='update-category'),
    path('del-category/<int:pk>', DeleteCategory.as_view(), name='del-category'),

    path('incomecash/', AddIncomeCash.as_view(), name='incomecash'),
    path('last-5-incomecash/', Last5IncomeCash.as_view(), name='last-5-income-cash'),
    path('sum-incomecash/', SumIncomeCash.as_view(), name='sum-income-cash'),
    path('sum-incomecash-group/', SumIncomeCashGroup.as_view(), name='sum-income-cash-group'),
    path('sum-monthly-income/', SumMonthlyIncomeView.as_view(), name='sum-monthly-income'),
    path('sum-monthly-percent-income/', SumPercentMonthlyIncomeView.as_view(), name='sum-percent-monthly-income'),
    path('update-incomecash/<int:pk>', UpdateIncomeCash.as_view(), name='update-income-cash'),
    path('delete-incomecash/<int:pk>', DeleteIncomeCash.as_view(), name='delete-income-cash'),

    path('outcomecash/', AddOutcomeCash.as_view(), name='outcome-cash'),
    path('last-5-outcomecash/', Last5OutcomeCash.as_view(), name='last-5-outcome-cash'),
    path('sum-outcomecash/', SumOutcomeCash.as_view(), name='sum-outcome-cash'),
    path('sum-outcomecash-group/', SumOutcomeCashGroup.as_view(), name='sum-outcome-cash-group'),
    path('sum-monthly-outcome/', SumMonthlyOutcomeView.as_view(), name='sum-monthly-outcome'),
    path('sum-monthly-percent-outcome/', SumPercentMonthlyOutcomeView.as_view(), name='sum-percent-monthly-outcome'),
    path('update-outcomecash/<int:pk>', UpdateOutcomeCash.as_view(), name='update-outcome-cash'),
    path('delete-outcomecash/<int:pk>', DeleteOutcomeCash.as_view(), name='delete-outcome-cash'),

    path('balance/', BalanceAPIView.as_view(), name='balance'),

    path('money-box/', AddMoneyBox.as_view(), name='money-box'),
    path('last-5-money-box/', Last5MoneyBox.as_view(), name='last-5-money-box'),
    path('sum-money-box/', SumMoneyBox.as_view(), name='sum-money-box'),
    path('sum-money-box-group/', SumMoneyBoxGroup.as_view(), name='sum-money-box-group'),
    path('sum-monthly-money-box/', SumMonthlyMoneyBoxView.as_view(), name='sum-monthly-money-box'),
    path('sum-monthly-percent-money-box/', SumPercentMonthlyMoneyBoxView.as_view(), name='sum-percent-monthly-money-box'),
    path('update-money-box/<int:pk>', UpdateMoneyBox.as_view(), name='update-money-box'),
    path('delete-money-box/<int:pk>', DeleteMoneyBox.as_view(), name='delete-money-box'),

    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('api/get-users/', GetUsers.as_view(), name='get-users'),
    # path('api/', include(router.urls)),
    # path('api/registration/', CreateUser.as_view(), name='create-user'),
    # path('api/drf-auth/', include('rest_framework.urls'))
]
