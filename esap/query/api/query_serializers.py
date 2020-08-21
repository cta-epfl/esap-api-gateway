
from rest_framework import serializers

# pagination for the 'esap-api/query/get-services request
class ServiceSerializer(serializers.Serializer):

    id = serializers.CharField()
    title = serializers.CharField()
    # description = serializers.CharField()
    service_type = serializers.CharField()
    access_url = serializers.CharField()
    short_name = serializers.CharField()
    content_types = serializers.CharField()
    waveband = serializers.CharField()

class Meta:
        fields = '__all__'