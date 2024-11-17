from __future__ import annotations

from rest_framework.generics import ListAPIView

from api.models import Country
from api.serializers.country import CountrySerializer


class CountriesApiView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
