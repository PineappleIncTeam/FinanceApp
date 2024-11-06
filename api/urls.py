from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path

from api.views import (CustomTokenCreateAPI,
                       CategoriesListCreateAPI,
                       CategoryUpdateDestroyAPI,
                       OperationListCreateAPI,
                       OperationRetrieveUpdateDestroyAPI,
                       password_reset_api_controller)

urlpatterns = [
    path(
        "auth/token/login/",
        CustomTokenCreateAPI.as_view(),
        name="login",
    ),
    path(
        "auth/",
        include("djoser.urls"),
    ),
    re_path(
        r"^auth/",
        include("djoser.urls.authtoken"),
    ),
    path(
        "password/reset/confirm/",
        password_reset_api_controller,
        name="reset-password",
    ),
    # CATEGORIES
    path(
        "categories/",
        CategoriesListCreateAPI.as_view(),
        name="categories",
    ),
    path(
        "categories/<int:pk>/",
        CategoryUpdateDestroyAPI.as_view(),
        name="category-info",
    ),
    # OPERATIONS
    path(
        "operations/",
        OperationListCreateAPI.as_view(),
        name="operations-list-create",
    ),
    path(
        "operations/<int:pk>/",
        OperationRetrieveUpdateDestroyAPI.as_view(),
        name="operations-detail",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
