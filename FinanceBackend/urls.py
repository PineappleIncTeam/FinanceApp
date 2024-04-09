from django.contrib import admin
from django.urls import path, include
from .spectacular import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
]

urlpatterns += doc_urls
