from __future__ import annotations


from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.models import Country
from api.serializers.countries import CountriesSerializer


class CountriesApiView(ListCreateAPIView):
    serializer_class = CountriesSerializer

    def get(self):
        countries = Country.objects.all()
        return countries
