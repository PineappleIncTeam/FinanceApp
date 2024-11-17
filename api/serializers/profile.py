from drf_extra_fields.fields import Base64ImageField
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from api.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False)

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "gender", "country", "country_name", "avatar"]
        read_only_fields = ["country_name"]

    @extend_schema_field(serializers.CharField())
    def get_country_name(self, obj):
        return obj.country.name if obj.country else None

    def update(self, instance, validated_data):
        new_avatar = validated_data.get('avatar', None)

        if new_avatar is None and instance.avatar:
            if instance.avatar:
                instance.avatar.delete(save=False)

        return super().update(instance, validated_data)