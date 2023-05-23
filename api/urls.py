from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

urlpatterns = [
    path('categories/', GetCreateCategoryAPIView.as_view(), name='categories'),
    path('income-categories/', GetIncomeCategories.as_view(), name='income-categories'),
    path('outcome-categories/', GetOutcomeCategories.as_view(), name='outcome-categories'),
    path('update-category/<int:pk>', UpdateCategory.as_view(), name='update-category'),
    path('del-category/<int:pk>', DeleteCategory.as_view(), name='del-category'),

    path('incomecash/', AddIncomeCash.as_view(), name='incomecash'),
    path('last-5-incomecash/', Last5IncomeCash.as_view(), name='last-5-incomecash'),
    path('sum-incomecash/', SumIncomeCash.as_view(), name='sum-incomecash'),
    path('sum-incomecash-group/', SumIncomeCashGroup.as_view(), name='sum-incomecash-group'),
    path('sum-monthly-income/', SumMonthlyIncomeView.as_view(), name='sum-monthly_income'),
    path('sum-monthly-percent-income/', SumPercentMonthlyIncomeView.as_view(), name='sum-percent-monthly_income'),
    path('update-incomecash/<int:pk>', UpdateIncomeCash.as_view(), name='update-incomecash'),
    path('delete-incomecash/<int:pk>', DeleteIncomeCash.as_view(), name='delete-incomecash'),

    path('outcomecash/', AddOutcomeCash.as_view(), name='outcomecash'),
    path('last-5-outcomecash/', Last5OutcomeCash.as_view(), name='last-5-outcomecash'),
    path('sum-outcomecash/', SumOutcomeCash.as_view(), name='sum-outcomecash'),
    path('sum-outcomecash-group/', SumOutcomeCashGroup.as_view(), name='sum-outcomecash-group'),
    path('sum-monthly-outcome/', SumMonthlyOutcomeView.as_view(), name='sum-monthly_outcome'),
    path('sum-monthly-percent-outcome/', SumPercentMonthlyOutcomeView.as_view(), name='sum-percent-monthly_outcome'),
    path('update-outcomecash/<int:pk>', UpdateOutcomeCash.as_view(), name='update-outcomecash'),
    path('delete-outcomecash/<int:pk>', DeleteOutcomeCash.as_view(), name='delete-outcomecash'),

    path('balance/', BalanceAPIView.as_view(), name='balance'),

    path('money-box/', MoneyBoxView.as_view(), name='money-box'),
    path('last-5-money-box/', Last5MoneyBox.as_view(), name='last-5-money-box'),
    path('delete-money-box/<int:pk>', DeleteMoneyBox.as_view(), name='delete-money-box'),

    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('api/get-users/', GetUsers.as_view(), name='get-users'),
    # path('api/', include(router.urls)),
    # path('api/registration/', CreateUser.as_view(), name='create-user'),
    # path('api/drf-auth/', include('rest_framework.urls'))
]
