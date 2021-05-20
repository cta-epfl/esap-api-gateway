import logging
from django.contrib import auth
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from ..models import *
from django.conf import settings

logger = logging.getLogger(__name__)

class EsapQuerySchemaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows EsapQuerySchemas to be viewed or edited.
    """

    queryset = EsapQuerySchema.objects.all().order_by("schema_name")
    serializer_class = EsapQuerySchemaSerializer
    permission_classes = [permissions.AllowAny]


class EsapComputeResourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows EsapComputeResources to be viewed or edited.
    """

    queryset = EsapComputeResource.objects.all().order_by("resource_name")
    serializer_class = EsapComputeResourceSerializer
    permission_classes = [permissions.AllowAny]


class EsapSoftwareRepositoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows EsapSoftwareRepositorys to be viewed or edited.
    """

    queryset = EsapSoftwareRepository.objects.all().order_by("repository_name")
    serializer_class = EsapSoftwareRepositorySerializer
    permission_classes = [permissions.AllowAny]


class EsapShoppingItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows EsapShoppingItems to be viewed or edited.
    """

    queryset = EsapShoppingItem.objects.all()
    serializer_class = EsapShoppingItemSerializer
    permission_classes = [permissions.AllowAny]


class EsapUserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows EsapUserProfiles to be viewed or edited.
    """

    queryset = EsapUserProfile.objects.all().order_by("user_name")
    serializer_class = EsapUserProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Returns nothing if no user_name supplied instead of all
        print("EsapUserProfileViewSet.get_queryset()")

        try:
            try:
                id_token = self.request.session["oidc_id_token"]
            except:
                id_token = None

            #uid = id_token["iss"]+id_token["sub"]
            #preferred_username = id_token["preferred_username"]
            #name = id_token["name"]
            #access_token = self.request.session["oidc_access_token"]

#            if settings.IS_DEV:
#                try:
#                    user = auth.get_user(self.request)
#                    user_email = user.email
#
#                except:
#                    # hardcode, because I don't get FAA to work in dev
#                    # 401 Client Error: Unauthorized for url: https://iam-escape.cloud.cnaf.infn.it/token
#                    user_email = "vermaas@astron.nl"
#            else:
            user = auth.get_user(self.request)
            user_email = user.email

            return EsapUserProfile.objects.filter(user_email=user_email)

        except AttributeError as e:
            print('ERROR: '+str(e))
            user_name = self.request.query_params.get("user_name", None)
            return EsapUserProfile.objects.filter(user_name=user_name)

#    def update(self, request, pk=None):
#        self.update()