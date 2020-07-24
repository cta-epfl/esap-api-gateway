from rest_framework import serializers
from ..models import Ida
import logging

logger = logging.getLogger(__name__)

class IdaSerializer(serializers.ModelSerializer):
    class Meta():
        model = Ida
        fields = "__all__"