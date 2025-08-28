from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from api.views import (
    CategoriesListCreateAPI,
    CategoryUpdateDestroyAPI,
    CountriesApiView,
    OperationListCreateAPI,
    OperationRetrieveUpdateDestroyAPI,
    ProfileApiView,
    ReportBalanceView,
    ReportCategoriesView,
    ReportStatisticsView,
    TargetMoneyReturnAPI,
    TargetsListCreateAPI,
    TargetUpdateDestroyAPI,
    PasswordResetConfirmView,
    VKOAuth2View,
    CurrencyDataView,
    OperationAllView,
    CustomLogoutView,
    OperationPDFView,
    OperationXLSView,
    TokenRefreshView,
    LoginView,
    ChequeView,
    CategoryGetAPI,
)

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("auth/logout/", CustomLogoutView.as_view(), name="custom-logout"),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="reset-password"),

    path("targets/", TargetsListCreateAPI.as_view(), name="targets"),
    path("targets/<int:pk>/", TargetUpdateDestroyAPI.as_view(), name="target-info"),
    path("targets/<int:pk>/return_money/", TargetMoneyReturnAPI.as_view(), name="target-money-return"),
    path("categories/", CategoriesListCreateAPI.as_view(), name="categories"),
    path("categories/all/", CategoryGetAPI.as_view()),
    path("categories/<int:pk>/", CategoryUpdateDestroyAPI.as_view(), name="category-info"),

    path("operations/", OperationListCreateAPI.as_view(), name="operations-list-create"),
    path("operations/all/", OperationAllView.as_view(), name="operations-list"),
    path("operations/<int:pk>/", OperationRetrieveUpdateDestroyAPI.as_view(), name="operations-detail"),

    path("countries/", CountriesApiView.as_view(), name="countries"),

    path("profile/", ProfileApiView.as_view(), name="profile"),
    
    path("reports/balance/", ReportBalanceView.as_view(), name="report-balance"),
    path("reports/categories/", ReportCategoriesView.as_view(), name="report-categories"),
    path("reports/statistics/", ReportStatisticsView.as_view(), name="report-statistics"),
  
    path("vkauth/", VKOAuth2View.as_view(), name="vkauth"),
  
    path("currency/", CurrencyDataView.as_view(), name="exchange-rates"),
  
    path("import/pdf/", OperationPDFView.as_view(), name="import_pdf"),
    path("import/xls/", OperationXLSView.as_view(), name="import_xls"),
  
    path("cheque", ChequeView.as_view(), name="cheque info"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
