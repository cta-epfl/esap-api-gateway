from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from .models import EsapUserProfile

def update_userprofile(claims):
    # check if a user already has a userprofile (by e-mail)
    user_email = claims['email']
    try:
        user = EsapUserProfile.objects.get(user_email=user_email)
    except:
        # to get more claims than just email, the 'profile' scope must be enabled in settings
        # OIDC_RP_SCOPES = "openid email profile"
        #uid = claims['iss'] + claims['sub']
        sub = claims['sub']
        user_name = claims['preferred_username']
        full_name= claims['name']
        new_user = EsapUserProfile(user_name=user_name, full_name=full_name, user_email=user_email)
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