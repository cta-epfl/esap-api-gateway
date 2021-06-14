from rest_framework import serializers

from ..models import *
import json

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
    shopping_cart = EsapShoppingItemSerializer(
        many=True,
        # view_name="shopping-items",
        read_only=False,
        # queryset=EsapShoppingItem.objects.all(),
    )

    def update(self, instance, validated_data):
        # Do not allow the user name to be updated - it is the primary key
        _ = validated_data.pop("user_name", None)

        for m2m_field in [
            "software_repositories",
            "compute_resources",
            "shopping_cart",
        ]:
            field_data = validated_data.pop(m2m_field, None)
            if field_data is not None:
                if len(field_data[0]) == 0:
                    raise RuntimeError(f"WTF! {validated_data}")
                field_instances = [
                    getattr(instance, m2m_field).model.objects.create(
                        # item_data=str(dict(field_datum))
                        item_data=json.dumps(dict(field_datum))
                    )
                    for field_datum in field_data
                ]
                print(field_instances)

                # make sure that the old entries are removed first, because
                getattr(instance, m2m_field).clear()
                getattr(instance, m2m_field).add(*field_instances)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        for m2m_field in [
            "software_repositories",
            "compute_resources",
            "shopping_cart",
        ]:
            field_data = data.get(m2m_field, None)
            if field_data is not None:
                internal_value.update({m2m_field: field_data})
        return internal_value

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
