from rest_framework import serializers

from rucio.models import Staging


class StagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staging
        fields = '__all__'