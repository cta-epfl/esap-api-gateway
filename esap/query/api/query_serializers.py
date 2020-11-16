
from rest_framework import serializers

# serialization for the 'esap-api/query/query request
class CreateAndRunQuerySerializer(serializers.Serializer):
    dataset = serializers.CharField()
    result = serializers.CharField()
    query = serializers.CharField()
    url = serializers.CharField()
    thumbnail = serializers.CharField()
    # fieldnames = serializers.CharField()
    # row = serializers.CharField()

class Meta:
        fields = '__all__'


# serialization for the 'esap-api/query/get-services request
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


# serialization for the 'esap-api/query/get-tables-fields request
class TablesFieldSerializer(serializers.Serializer):

    table_name = serializers.CharField()
    table_type = serializers.CharField()
    fields     = serializers.ListField()

class Meta:
        fields = '__all__'