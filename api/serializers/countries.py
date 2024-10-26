from rest_framework import serializers

from api.models import Countries


class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = ['code', 'name', 'full_name']