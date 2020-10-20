from rest_framework import viewsets
from .serializers import *
from ..models import *


class EsapQuerySchemaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows EsapQuerySchemas to be viewed or edited.
    """

    queryset = EsapQuerySchema.objects.all().order_by("schema_name")
    serializer_class = EsapQuerySchemaSerializer
    permission_classes = []


class EsapComputeResourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows EsapComputeResources to be viewed or edited.
    """

    queryset = EsapComputeResource.objects.all().order_by("resource_name")
    serializer_class = EsapComputeResourceSerializer
    permission_classes = []


class EsapSoftwareRepositoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows EsapSoftwareRepositorys to be viewed or edited.
    """

    queryset = EsapSoftwareRepository.objects.all().order_by("repository_name")
    serializer_class = EsapSoftwareRepositorySerializer
    permission_classes = []


class EsapShoppingItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows EsapShoppingItems to be viewed or edited.
    """

    queryset = EsapShoppingItem.objects.all()
    serializer_class = EsapShoppingItemSerializer
    permission_classes = []


class EsapUserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows EsapUserProfiles to be viewed or edited.
    """

    queryset = EsapUserProfile.objects.all().order_by("user_name")
    serializer_class = EsapUserProfileSerializer
    permission_classes = []

    def get_queryset(self):
        # Returns nothing if no user_name supplied instead of all
        user_name = self.request.query_params.get("user_name", None)
        return EsapUserProfile.objects.filter(user_name=user_name)
