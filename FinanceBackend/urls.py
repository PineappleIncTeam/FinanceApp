from django.contrib import admin
from django.urls import path, include, re_path
from .yasg import urlpatterns as doc_urls
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),

]

urlpatterns += doc_urls
