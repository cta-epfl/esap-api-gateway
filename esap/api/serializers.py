from rest_framework import serializers
from .models import AdexBaseObject, DataSet, Archive
import logging

logger = logging.getLogger(__name__)

class AdexBaseObjectSerializer(serializers.ModelSerializer):
    class Meta():
        model = AdexBaseObject
        fields = "__all__"


# this is a serializer that uses hyperlinks to produce a navigable REST API
class DataSetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta():
        model = DataSet
        fields = "__all__"


# this is a serializer that uses uri's in the datasets for easier identification for the frontend
class DataSetModelSerializer(serializers.ModelSerializer):

    # show the uri of the archive (
    data_archive = serializers.StringRelatedField(
        many=False,
        required=False,
    )

    class Meta():
        model = DataSet
        fields = "__all__"


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

        # note: "__all__" cannot be ussed because the id is also used in the frontend, and not automatically returned
        # note: 'datasets' is a special field, it is the 'datasets.data_archive' relationship also serialized in Archive
        fields = ('id', 'uri', 'name', 'short_description', 'long_description', 'retrieval_description', 'thumbnail',
                   'documentation_url','instrument','catalog_name','catalog_url','datasets')


# this is a serializer that uses uri's in the datasets for easier identification for the frontend
class ArchiveModelSerializer(serializers.ModelSerializer):

    datasets = serializers.StringRelatedField(
        many=True,
        required=False,
    )

    class Meta():
        model = Archive

        # note: "__all__" cannot be ussed because the id is also used in the frontend, and not automatically returned
        # note: 'datasets' is a special field, it is the 'datasets.data_archive' relationship also serialized in Archive
        fields = ('id', 'uri', 'name', 'short_description', 'long_description', 'retrieval_description', 'thumbnail',
                   'documentation_url','instrument','catalog_name','catalog_url','datasets')
