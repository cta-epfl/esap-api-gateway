from mozilla_django_oidc.auth import OIDCAuthenticationBackend

class MyOIDCAB(OIDCAuthenticationBackend):

    # this is an example of overriding a part of the Authentication backend
    def verify_claims(self, claims):
        print('MyOIDCAB.verify_claims('+str(claims)+')')
        verified = super(MyOIDCAB, self).verify_claims(claims)
        is_admin = 'admin' in claims.get('group', [])
        return True
        # return verified and is_admin