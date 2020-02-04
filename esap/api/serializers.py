from rest_framework import serializers
from .models import EsapBaseObject, DataSet, Archive, Catalog, ParameterMapping
import logging

logger = logging.getLogger(__name__)

class AdexBaseObjectSerializer(serializers.ModelSerializer):
    class Meta():
        model = EsapBaseObject
        fields = "__all__"


# this is a serializer that uses hyperlinks to produce a navigable REST API
class DataSetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta():
        model = DataSet
        fields = "__all__"


# this is a serializer that uses uri's in the datasets for easier identification for the frontend
class DataSetModelSerializer(serializers.ModelSerializer):


    class Meta():
        model = DataSet
        # fields = "__all__"
        fields = ('id', 'uri', 'name', 'short_description','long_description', 'retrieval_description', 'thumbnail',
                   'documentation_url', 'archive_name_derived',
                  'archive_uri_derived','catalog_name_derived','catalog_uri_derived')


# this is a serializer that uses hyperlinks to produce a navigable REST API
class ArchiveSerializer(serializers.HyperlinkedModelSerializer):

    datasets = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        # read_only=False
        # queryset=DataSet.objects.all(),
        view_name='dataset-detail',
        lookup_field='pk',
        required=False
    )

    class Meta():
        model = Archive

        fields = ('id', 'uri', 'name', 'short_description', 'long_description', 'retrieval_description', 'thumbnail',
                   'documentation_url','instrument','institute','datasets')


# this is a serializer that uses uri's in the datasets for easier identification for the frontend
class ArchiveModelSerializer(serializers.ModelSerializer):

    datasets = serializers.StringRelatedField(
        many=True,
        required=False,
    )

    class Meta():
        model = Archive

        fields = ('id', 'uri', 'name', 'short_description', 'long_description', 'retrieval_description', 'thumbnail',
                   'documentation_url','instrument','institute','datasets')


# this is a serializer that uses hyperlinks to produce a navigable REST API
class CatalogSerializer(serializers.HyperlinkedModelSerializer):

    dataset = serializers.HyperlinkedRelatedField(
        many=False,
        required=False,
        read_only=True,
        view_name='dataset-detail',
        lookup_field='pk',
    )

    parameters = serializers.HyperlinkedRelatedField(
        many=False,
        required=False,
        read_only=True,
        view_name='parametermapping-detail',
        lookup_field='pk',
    )

    class Meta():
        model = Catalog
        # fields = "__all__"
        fields = ('id', 'uri', 'name', 'short_description', 'long_description', 'retrieval_description', 'thumbnail',
                    'url', 'dataset', 'parameters', 'parameters')

# this is a serializer that uses hyperlinks to produce a navigable REST API
class ParameterMappingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta():
        model = ParameterMapping
        fields = "__all__"