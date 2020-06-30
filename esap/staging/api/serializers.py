from rest_framework import serializers
from ..models import Staging
import logging

logger = logging.getLogger(__name__)

class StagingSerializer(serializers.ModelSerializer):
    class Meta():
        model = Staging
        fields = "__all__"