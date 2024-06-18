from rest_framework import serializers
from api.models import User, Country, City


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    city = CitySerializer()

    class Meta:
        model = User
        fields = ["id", "email", "username", "gender", "country", "city"]
