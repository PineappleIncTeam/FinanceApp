from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import (GetCreateCategoryAPIView,
                    DeleteCategory,
                    UpdateCategory,
                    AddIncomeCash,
                    Last5IncomeCash)


router = DefaultRouter()



urlpatterns = [
    # path('api/', include(router.urls)),
    # path('api/registration/', CreateUser.as_view(), name='create-user'),
    # path('api/drf-auth/', include('rest_framework.urls')),
    path('categories/', GetCreateCategoryAPIView.as_view(), name='categories'),
    path('update-category/<int:pk>', UpdateCategory.as_view(), name='update-category'),
    path('del-category/<int:pk>', DeleteCategory.as_view(), name='del-category'),
    path('incomecash/', AddIncomeCash.as_view(), name='incomecash'),
    path('last-5-incomecash/', Last5IncomeCash.as_view(), name='last-5-incomecash'),
    # path('api/get-users/', GetUsers.as_view(), name='get-users'),
    path('auth/', include('djoser.urls')),          # new
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # new
]
