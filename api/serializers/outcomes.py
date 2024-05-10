import logging

from rest_framework import serializers

from api.models import OutcomeCategories

logger = logging.getLogger(__name__)


class OutcomeCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomeCategories
        fields = ["id", "name"]
