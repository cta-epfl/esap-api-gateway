from rest_framework import serializers

from rucio.models import Rucio


class RucioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rucio
        fields = '__all__'