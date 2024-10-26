from __future__ import annotations

from django.db.models import QuerySet
from django.http import JsonResponse


from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.models import Countries
from api.serializers.countries import CountriesSerializer


class CountriesApiView(ListCreateAPIView):
    serializer_class = CountriesSerializer

    def get(self):
        countries = Countries.objects.all()
        return countries
