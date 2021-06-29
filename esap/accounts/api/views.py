import logging
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from ..models import *
import base64
import json

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

        user_profile = []
        try:
            try:
                id_token = self.request.session["oidc_id_token"]

                # a oidc_id_token has a header, payload and signature split by a '.'
                token = id_token.split('.')

                # add the "===" to avoid an "Incorrect padding" exception
                decoded_payload = base64.urlsafe_b64decode(token[1] + "===")
                decoded_token = json.loads(decoded_payload.decode("UTF-8"))

                uid = decoded_token["iss"] + 'userinfo:' + decoded_token["sub"]
                logger.info('uid = ' + uid)

                user_profile = EsapUserProfile.objects.filter(uid=uid)

                # save the current token to the user_profile (for transport and usage elsewhere)
                for profile in user_profile:
                    profile.oidc_id_token = id_token
                    profile.save()

                logger.info('user_profile = ' + str(user_profile))
            except Exception as error:
                logger.error(str(error))
                id_token = None

                # no AAI token found, try basic authentication (dev only)
                try:
                    user = self.request.user
                    user_email = user.email
                    user_profile = EsapUserProfile.objects.filter(user_email=user_email)
                except:
                    pass

            return user_profile

        except AttributeError as e:
            print('ERROR: '+str(e))
            user_name = self.request.query_params.get("user_name", None)
            return EsapUserProfile.objects.filter(user_name=user_name)
