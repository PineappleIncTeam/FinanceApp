from __future__ import annotations


from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Country


class CountriesApiView(APIView):
    def get(self, request):
        countries = Country.objects.all().values()
        return Response(countries)


