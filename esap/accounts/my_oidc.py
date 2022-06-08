import logging
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from django.conf import settings

from .models import EsapUserProfile
logger = logging.getLogger(__name__)

def update_userprofile(claims):
    # check if a user already has a userprofile (by unique id)
    uid = settings.OIDC_OP_USER_ENDPOINT + ":" + claims['sub']
    logger.info('update_userprofile uid = ' + uid)
    try:
        user = EsapUserProfile.objects.get(uid=uid)
    except:
        # to get more claims than just email, the 'profile' scope must be enabled in settings
        # OIDC_RP_SCOPES = "openid email profile"

        uid = settings.OIDC_OP_USER_ENDPOINT + ":" + claims['sub']
        user_email = claims['email']

        user_name = claims.get('preferred_username', None)

        if user_name is None:
            user_name = claims.get('nickname', None)

        if user_name is None:
            user_name = user_email

        logger.info('user_name (from claims[preferred_username]) = ' + user_name)
        full_name= claims['name']

        logger.info('full_name (from claims[name]) = ' + full_name)
        new_user = EsapUserProfile(user_name=user_name, full_name=full_name, user_email=user_email, uid=uid)
        new_user.save()


class MyOIDCAB(OIDCAuthenticationBackend):
    # https://mozilla-django-oidc.readthedocs.io/en/stable/installation.html#changing-how-django-users-are-created

    # this is an example of overriding a part of the Authentication backend
    def verify_claims(self, claims):
        print('MyOIDCAB.verify_claims('+str(claims)+')')

        update_userprofile(claims)

        verified = super(MyOIDCAB, self).verify_claims(claims)
        is_admin = 'admin' in claims.get('group', [])
        return verified
        # return verified and is_admin


