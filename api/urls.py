from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path

from api.views import (BalanceGetAPI, CustomTokenCreateAPI,
                       OperationListCreateAPI,
                       OperationRetrieveUpdateDestroyAPI,
                       activate_users_api_controller,
                       password_reset_api_controller)

urlpatterns = [
    path("auth/token/login/", CustomTokenCreateAPI.as_view(), name="login"),
    path("auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("activate/", activate_users_api_controller, name="activate-users"),
    path(
        "password/reset/confirm/", password_reset_api_controller, name="reset-password"
    ),
    # BALANCE
    path("balance/", BalanceGetAPI.as_view(), name="balance"),
    # OPERATIONS
    path(
        "operations/", OperationListCreateAPI.as_view(), name="operations-list-create"
    ),
    path(
        "operations/<int:pk>/",
        OperationRetrieveUpdateDestroyAPI.as_view(),
        name="operations-detail",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
