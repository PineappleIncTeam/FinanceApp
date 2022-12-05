from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import (GetCreateCategoryAPIView,
                    DeleteCategory,
                    UpdateCategory,
                    GetIncomeCategories,
                    GetOutcomeCategories,
                    AddIncomeCash,
                    AddOutcomeCash,
                    Last5IncomeCash,
                    Last5OutcomeCash,
                    SumIncomeCash,
                    SumOutcomeCash,
                    BalanceAPIView,
                    UpdateIncomeCash,
                    UpdateOutcomeCash,
                    DeleteIncomeCash,
                    DeleteOutcomeCash)

router = DefaultRouter()

urlpatterns = [
    # path('api/', include(router.urls)),
    # path('api/registration/', CreateUser.as_view(), name='create-user'),
    # path('api/drf-auth/', include('rest_framework.urls')),
    path('categories/', GetCreateCategoryAPIView.as_view(), name='categories'),
    path('income-categories/', GetIncomeCategories.as_view(), name='income-categories'),
    path('outcome-categories/', GetOutcomeCategories.as_view(), name='outcome-categories'),
    path('update-category/<int:pk>', UpdateCategory.as_view(), name='update-category'),
    path('del-category/<int:pk>', DeleteCategory.as_view(), name='del-category'),
    path('incomecash/', AddIncomeCash.as_view(), name='incomecash'),
    path('update-incomecash/<int:pk>', UpdateIncomeCash.as_view(), name='update-incomecash'),
    path('delete-incomecash/<int:pk>', DeleteIncomeCash.as_view(), name='delete-incomecash'),
    path('outcomecash/', AddOutcomeCash.as_view(), name='outcomecash'),
    path('update-outcomecash/<int:pk>', UpdateOutcomeCash.as_view(), name='update-outcomecash'),
    path('delete-outcomecash/<int:pk>', DeleteOutcomeCash.as_view(), name='delete-outcomecash'),
    path('balance/', BalanceAPIView.as_view(), name='balance'),
    path('last-5-incomecash/', Last5IncomeCash.as_view(), name='last-5-incomecash'),
    path('last-5-outcomecash/', Last5OutcomeCash.as_view(), name='last-5-outcomecash'),
    path('sum-incomecash/', SumIncomeCash.as_view(), name='sum-incomecash'),
    path('sum-outcomecash/', SumOutcomeCash.as_view(), name='sum-outcomecash'),
    # path('api/get-users/', GetUsers.as_view(), name='get-users'),
    path('auth/', include('djoser.urls')),  # new
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # new
]
