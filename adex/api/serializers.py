from rest_framework import serializers
from .models import DataSource
import logging

logger = logging.getLogger(__name__)

class DataSourceSerializer(serializers.ModelSerializer):
    class Meta():
        model = DataSource
        fields = "__all__"
