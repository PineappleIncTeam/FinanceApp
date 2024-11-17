from rest_framework import serializers
from api.models import Profile, Country


class ProfileSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "gender", "country", "country_name"]

    def get_country_name(self, obj):
        return obj.country.name if obj.country else None
