from rest_framework import serializers

from api.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "gender", "country", "country_name", "avatar"]

    def get_country_name(self, obj):
        return obj.country.name if obj.country else None

    def update(self, instance, validated_data):
        new_avatar = validated_data.get('avatar', None)

        if new_avatar is not None:
            if instance.avatar:
                instance.avatar.delete(save=False)

        return super().update(instance, validated_data)