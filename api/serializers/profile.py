from rest_framework import serializers
from api.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'gender', 'country', 'avatar']


