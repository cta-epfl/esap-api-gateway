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


class EsapShoppingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EsapShoppingItem
        fields = ["item_data","user_profile"]


class EsapUserProfileSerializer(serializers.HyperlinkedModelSerializer):

    # this adds a 'shopping_cart' list to the EsapUserProfile API.
    # note that 'shopping_cart' is not defined in the EsapUserProfile model,
    # but in the EsapShoppingItem model as foreignKey to get a 1-to-many relationship

    shopping_cart = EsapShoppingItemSerializer(
        many=True,
        required=False,
    )

    def update(self, instance, validated_data):
        # Do not allow the user name to be updated - it is the primary key

        _ = validated_data.pop("user_name", None)

        # shopping cart data is updated through the EsapUserProfileSerializer
        # because the EsapUserProfileViewSet holds the authentication logic.
        # But a reversed related field cannot be updated directly,
        # hence this construction in the update method of the serializer.

        # first remove all existing shopping items for this user,
        # because the incoming payload will contain all the active ones.
        existing_items = EsapShoppingItem.objects.filter(user_profile=instance)
        existing_items.delete()

        shopping_cart_data = validated_data['shopping_cart']
        for shopping_item_data in shopping_cart_data:

            shopping_cart_instance = EsapShoppingItem.objects.create(
                item_data=json.dumps(dict(shopping_item_data)),
                user_profile=instance
            )
            shopping_cart_instance.save()

        # shopping_cart has already been handled, remove from validated_data
        _ = validated_data.pop("shopping_cart", None)

        for m2m_field in [
            "software_repositories",
            "compute_resources",
            #"shopping_cart",
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

                # make sure that the old entries are removed first, to also allow removal of items
                # getattr(instance, m2m_field).clear()
                getattr(instance, m2m_field).add(*field_instances)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        for my_field in [
            "software_repositories",
            "compute_resources",
            "shopping_cart",
        ]:
            field_data = data.get(my_field, None)
            if field_data is not None:
                internal_value.update({my_field: field_data})
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
