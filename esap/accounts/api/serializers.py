from rest_framework import serializers

from ..models import *


class EsapQuerySchemaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EsapQuerySchema
        fields = ["schema_name"]


class EsapComputeResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EsapComputeResource
        fields = [
            "resource_name",
            "resource_type",
            "resource_url",  # 'resource_metadata'
        ]


class EsapSoftwareRepositorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EsapSoftwareRepository
        fields = [
            "repository_name",
            "repository_type",
            "repository_url",  #'repository_metadata'
        ]


class EsapShoppingItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EsapShoppingItem
        fields = ["item_data"]


class EsapUserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EsapUserProfile
        fields = [
            "user_name",
            "full_name",
            "user_email",
            "query_schema",
            "software_repositories",
            "compute_resources",
            "shopping_cart",
        ]
