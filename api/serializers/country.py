from rest_framework.serializers import ModelSerializer

from api.models import Country


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
