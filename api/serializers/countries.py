from rest_framework import serializers

from api.models import Country


class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['code', 'name', 'full_name']