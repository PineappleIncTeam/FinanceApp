from django.urls import path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    validators=['ssv', 'flex'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('api/v1/schema/', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    path(
        'api/v1/schema/swagger-ui/',
        schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path(
        'api/v1/schema/redoc/',
        schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]
